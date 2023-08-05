# SPDX-FileCopyrightText: 2023 Geoffrey Lentner
# SPDX-License-Identifier: Apache-2.0

"""
Connect to server and run tasks.

Example:
    >>> from hypershell.client import run_client
    >>> run_client(num_tasks=4, address=('<IP ADDRESS>', 8080), auth='<secret>')

Embed a `ClientThread` in your application directly. Call `stop()` to stop early.
Clients cannot connect to a remote machine unless you set the server's `bind` address
to 0.0.0.0 (as opposed to localhost which is the default).

Example:
    >>> from hypershell.client import ClientThread
    >>> client_thread = ClientThread.new(num_tasks=4, address=('<IP ADDRESS>', 8080), auth='<secret>')

Note:
    In order for the `ClientThread` to actively monitor the state set by `stop` and
    halt execution (a requirement because of how CPython does threading), the implementation
    uses a finite state machine. *You should not instantiate this machine directly*.

Warning:
    Because the `ClientThread` checks state actively to decide whether to halt, it may take
    some few moments before it shutsdown on its own. If your main program exits however,
    the thread will be stopped regardless because it runs as a `daemon`.
"""


# type annotations
from __future__ import annotations
from typing import List, Tuple, Optional, Callable, Dict, IO, Type
from types import TracebackType

# standard libs
import os
import sys
import time
import json
import random
import signal
import functools
from enum import Enum
from datetime import datetime, timedelta
from queue import Queue, Empty as QueueEmpty, Full as QueueFull
from subprocess import Popen, TimeoutExpired
from socket import gaierror
from dataclasses import dataclass
from multiprocessing import AuthenticationError

# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Namespace

# internal libs
from hypershell.data.model import Task
from hypershell.core.ansi import colorize_usage
from hypershell.core.heartbeat import Heartbeat, ClientState
from hypershell.core.platform import default_path
from hypershell.core.config import default, config, load_task_env
from hypershell.core.fsm import State, StateMachine
from hypershell.core.thread import Thread
from hypershell.core.queue import QueueClient, QueueConfig
from hypershell.core.logging import HOSTNAME, INSTANCE, Logger
from hypershell.core.template import Template, DEFAULT_TEMPLATE
from hypershell.core.exceptions import (handle_exception, handle_disconnect,
                                        handle_address_unknown, HostAddressInfo, get_shared_exception_mapping)

# public interface
__all__ = ['run_client', 'ClientThread', 'ClientApp', 'ClientInfo', 'DEFAULT_NUM_TASKS', 'DEFAULT_DELAY', ]

# initialize logger
log = Logger.with_name(__name__)


@dataclass
class ClientInfo:
    """Client instance ID/hostname and task ID mapping."""

    client_id: str
    client_host: str
    task_ids: List[str]

    @classmethod
    def from_dict(cls: Type[ClientInfo], data: dict) -> ClientInfo:
        """Initialize from existing dictionary."""
        return cls(**data)

    def to_dict(self: ClientInfo) -> dict:
        """Export to dictionary."""
        return {'client_id': self.client_id, 'client_host': self.client_host, 'task_ids': self.task_ids}

    def pack(self: ClientInfo) -> bytes:
        """Serialize data."""
        return json.dumps(self.to_dict()).encode('utf-8')

    @classmethod
    def unpack(cls: Type[ClientInfo], data: bytes) -> ClientInfo:
        """Deserialize from raw `data`."""
        return cls.from_dict(json.loads(data.decode('utf-8')))

    @classmethod
    def from_tasks(cls: Type[ClientInfo], tasks: List[Task]) -> ClientInfo:
        """Initialize from list of existing Task instances."""
        return cls(client_id=INSTANCE, client_host=HOSTNAME,
                   task_ids=[task.id for task in tasks])

    def transpose(self: ClientInfo) -> List[Dict[str, str]]:
        """Represent as list of dicts for database update."""
        return [{'id': task_id, 'client_id': self.client_id, 'client_host': self.client_host}
                for task_id in self.task_ids]


class SchedulerState(State, Enum):
    """Finite states for scheduler."""
    START = 0
    GET_REMOTE = 1
    UNPACK = 2
    PUT_CONFIRM = 3
    POP_TASK = 4
    PUT_LOCAL = 5
    FINAL = 6
    HALT = 7


class ClientScheduler(StateMachine):
    """Receive task bundles from server and schedule locally."""

    queue: QueueClient
    local: Queue[Optional[Task]]
    bundle: List[bytes]
    client_info: Optional[bytes]
    no_confirm: bool
    timeout: Optional[timedelta]

    previous_received: datetime

    task: Task
    tasks: List[Task]

    state = SchedulerState.START
    states = SchedulerState

    def __init__(self: ClientScheduler,
                 queue: QueueClient,
                 local: Queue[Optional[Task]],
                 no_confirm: bool = False,
                 timeout: int = None) -> None:
        """Assign remote queue client and local task queue."""
        self.queue = queue
        self.local = local
        self.bundle = []
        self.tasks = []
        self.client_info = None
        self.no_confirm = no_confirm
        self.timeout = None if not timeout else timedelta(seconds=timeout)
        self.previous_received = datetime.now()

    @functools.cached_property
    def actions(self: ClientScheduler) -> Dict[SchedulerState, Callable[[], SchedulerState]]:
        return {
            SchedulerState.START: self.start,
            SchedulerState.GET_REMOTE: self.get_remote,
            SchedulerState.UNPACK: self.unpack_bundle,
            SchedulerState.PUT_CONFIRM: self.put_confirm,
            SchedulerState.POP_TASK: self.pop_task,
            SchedulerState.PUT_LOCAL: self.put_local,
            SchedulerState.FINAL: self.finalize,
        }

    def start(self: ClientScheduler) -> SchedulerState:
        """Jump to GET_REMOTE state."""
        timeout_label = self.timeout or 'no'
        log.debug(f'Started (scheduler: {timeout_label} timeout)')
        return SchedulerState.GET_REMOTE

    def get_remote(self: ClientScheduler) -> SchedulerState:
        """Get the next task bundle from the server."""
        try:
            self.bundle = self.queue.scheduled.get(timeout=2)
            self.queue.scheduled.task_done()
            self.previous_received = datetime.now()
            if self.bundle is not None:
                log.debug(f'Received {len(self.bundle)} tasks ({HOSTNAME}: {INSTANCE})')
                return SchedulerState.UNPACK
            else:
                log.debug('Disconnect received')
                return SchedulerState.FINAL
        except QueueEmpty:
            waited = datetime.now() - self.previous_received
            if self.timeout is None or waited < self.timeout:
                return SchedulerState.GET_REMOTE
            else:
                log.debug(f'Timeout reached ({waited})')
                return SchedulerState.FINAL

    def unpack_bundle(self: ClientScheduler) -> SchedulerState:
        """Unpack latest bundle of tasks."""
        self.tasks = [Task.unpack(data) for data in self.bundle]
        if not self.no_confirm:
            self.client_info = ClientInfo.from_tasks(self.tasks).pack()
            return SchedulerState.PUT_CONFIRM
        else:
            return SchedulerState.POP_TASK

    def put_confirm(self: ClientScheduler) -> SchedulerState:
        """Put confirmation details back on remote queue."""
        try:
            self.queue.confirmed.put(self.client_info, timeout=2)
            log.debug(f'Confirmed {len(self.tasks)} tasks ({HOSTNAME}: {INSTANCE})')
            return SchedulerState.POP_TASK
        except QueueFull:
            return SchedulerState.PUT_CONFIRM

    def pop_task(self: ClientScheduler) -> SchedulerState:
        """Pop next task off current task list."""
        try:
            self.task = self.tasks.pop(0)
            return SchedulerState.PUT_LOCAL
        except IndexError:
            return SchedulerState.GET_REMOTE

    def put_local(self: ClientScheduler) -> SchedulerState:
        """Put latest task on the local task queue."""
        try:
            self.local.put(self.task, timeout=2)
            return SchedulerState.POP_TASK
        except QueueFull:
            return SchedulerState.PUT_LOCAL

    @staticmethod
    def finalize() -> SchedulerState:
        """Stop scheduler."""
        log.debug('Done (scheduler)')
        return SchedulerState.HALT


class ClientSchedulerThread(Thread):
    """Run client scheduler in dedicated thread."""

    def __init__(self: ClientSchedulerThread,
                 queue: QueueClient,
                 local: Queue[Optional[bytes]],
                 no_confirm: bool = False,
                 timeout: int = None) -> None:
        """Initialize machine."""
        super().__init__(name='hypershell-client-scheduler')
        self.machine = ClientScheduler(queue=queue, local=local, no_confirm=no_confirm, timeout=timeout)

    def run_with_exceptions(self: ClientSchedulerThread) -> None:
        """Run machine."""
        self.machine.run()

    def stop(self: ClientSchedulerThread, wait: bool = False, timeout: int = None) -> None:
        """Stop machine."""
        log.warning('Stopping (scheduler)')
        self.machine.halt()
        super().stop(wait=wait, timeout=timeout)


DEFAULT_BUNDLESIZE: int = default.client.bundlesize
DEFAULT_BUNDLEWAIT: int = default.client.bundlewait


class CollectorState(State, Enum):
    """Finite states of collector."""
    START = 0
    GET_LOCAL = 1
    CHECK_BUNDLE = 2
    PACK_BUNDLE = 3
    PUT_REMOTE = 4
    FINAL = 5
    HALT = 6


class ClientCollector(StateMachine):
    """Collect finished tasks and bundle for outgoing queue."""

    tasks: List[Task]
    bundle: List[bytes]

    queue: QueueClient
    local: Queue[Optional[Task]]

    bundlesize: int
    bundlewait: int
    previous_send: datetime

    state = CollectorState.START
    states = CollectorState

    def __init__(self: ClientCollector, queue: QueueClient, local: Queue[Optional[Task]],
                 bundlesize: int = DEFAULT_BUNDLESIZE, bundlewait: int = DEFAULT_BUNDLEWAIT) -> None:
        """Collect tasks from local queue of finished tasks and push them to the server."""
        self.tasks = []
        self.bundle = []
        self.local = local
        self.queue = queue
        self.bundlesize = bundlesize
        self.bundlewait = bundlewait

    @functools.cached_property
    def actions(self: ClientCollector) -> Dict[CollectorState, Callable[[], CollectorState]]:
        return {
            CollectorState.START: self.start,
            CollectorState.GET_LOCAL: self.get_local,
            CollectorState.CHECK_BUNDLE: self.check_bundle,
            CollectorState.PACK_BUNDLE: self.pack_bundle,
            CollectorState.PUT_REMOTE: self.put_remote,
            CollectorState.FINAL: self.finalize,
        }

    def start(self: ClientCollector) -> CollectorState:
        """Jump to GET_LOCAL state."""
        log.debug('Started (collector)')
        self.previous_send = datetime.now()
        return CollectorState.GET_LOCAL

    def get_local(self: ClientCollector) -> CollectorState:
        """Get the next task from the local completed task queue."""
        try:
            task = self.local.get(timeout=1)
            self.local.task_done()
            if task:
                self.tasks.append(task)
                return CollectorState.CHECK_BUNDLE
            else:
                return CollectorState.FINAL
        except QueueEmpty:
            return CollectorState.CHECK_BUNDLE

    def check_bundle(self: ClientCollector) -> CollectorState:
        """Check state of task bundle and proceed with return if necessary."""
        wait_time = (datetime.now() - self.previous_send)
        since_last = wait_time.total_seconds()
        if len(self.tasks) >= self.bundlesize:
            log.trace(f'Bundle size reached ({len(self.tasks)} tasks)')
            return CollectorState.PACK_BUNDLE
        elif since_last >= self.bundlewait:
            log.trace(f'Bundle wait exceeded ({wait_time})')
            return CollectorState.PACK_BUNDLE
        else:
            return CollectorState.GET_LOCAL

    def pack_bundle(self: ClientCollector) -> CollectorState:
        """Pack tasks into bundle before pushing back to server."""
        self.bundle = [task.pack() for task in self.tasks]
        return CollectorState.PUT_REMOTE

    def put_remote(self: ClientCollector) -> CollectorState:
        """Push out bundle of completed tasks."""
        if self.bundle:
            self.queue.completed.put(self.bundle)
            log.trace(f'Bundle returned ({len(self.bundle)} tasks)')
            self.tasks.clear()
            self.bundle.clear()
            self.previous_send = datetime.now()
        else:
            log.trace('Bundle empty')
        return CollectorState.GET_LOCAL

    def finalize(self: ClientCollector) -> CollectorState:
        """Push out any remaining tasks and halt."""
        self.put_remote()
        log.debug('Done (collector)')
        return CollectorState.HALT


class ClientCollectorThread(Thread):
    """Run client collector within dedicated thread."""

    def __init__(self: ClientCollectorThread, queue: QueueClient, local: Queue[Optional[bytes]],
                 bundlesize: int = DEFAULT_BUNDLESIZE, bundlewait: int = DEFAULT_BUNDLEWAIT) -> None:
        """Initialize machine."""
        super().__init__(name='hypershell-client-collector')
        self.machine = ClientCollector(queue=queue, local=local, bundlesize=bundlesize, bundlewait=bundlewait)

    def run_with_exceptions(self: ClientCollectorThread) -> None:
        """Run machine."""
        self.machine.run()

    def stop(self: ClientCollectorThread, wait: bool = False, timeout: int = None) -> None:
        """Stop machine."""
        log.warning('Stopping (collector)')
        self.machine.halt()
        super().stop(wait=wait, timeout=timeout)


def task_env(task: Task) -> Dict[str, str]:
    """Build environment dictionary for the given `task`."""
    task_data = task.to_json()
    task_data.pop('tag')  # do not include tags in environ
    return {
        **os.environ,
        **load_task_env(),
        **Namespace.from_dict(task_data).to_env().flatten(prefix='TASK'),
        'TASK_CWD': config.task.cwd,
        'TASK_OUTPATH': os.path.join(default_path.lib, 'task', f'{task.id}.out'),
        'TASK_ERRPATH': os.path.join(default_path.lib, 'task', f'{task.id}.err'),
    }


class TaskState(State, Enum):
    """Finite states for task executor."""
    START = 0
    GET_LOCAL = 1
    CREATE_TASK = 2
    START_TASK = 3
    WAIT_TASK = 4
    STOP_TASK = 5
    TERM_TASK = 6
    KILL_TASK = 7
    PUT_LOCAL = 8
    FINAL = 9
    HALT = 10


class TaskExecutor(StateMachine):
    """Run tasks locally."""

    id: int
    task: Task
    process: Popen
    template: Template
    redirect_output: IO
    redirect_errors: IO
    capture: bool

    timeout: Optional[int]
    attempted_sigint: bool
    attempted_sigterm: bool
    attempted_sigkill: bool

    inbound: Queue[Optional[Task]]
    outbound: Queue[Optional[Task]]

    state = TaskState.START
    states = TaskState

    def __init__(self: TaskExecutor,
                 id: int,
                 inbound: Queue[Optional[Task]],
                 outbound: Queue[Optional[Task]],
                 template: str = DEFAULT_TEMPLATE,
                 redirect_output: IO = None,
                 redirect_errors: IO = None,
                 capture: bool = False,
                 timeout: int = None) -> None:
        """Initialize task executor."""
        self.id = id
        self.template = Template(template)
        self.inbound = inbound
        self.outbound = outbound
        self.redirect_output = redirect_output or sys.stdout
        self.redirect_errors = redirect_errors or sys.stderr
        self.capture = capture
        self.timeout = timeout

    @functools.cached_property
    def actions(self: TaskExecutor) -> Dict[TaskState, Callable[[], TaskState]]:
        return {
            TaskState.START: self.start,
            TaskState.GET_LOCAL: self.get_local,
            TaskState.CREATE_TASK: self.create_task,
            TaskState.START_TASK: self.start_task,
            TaskState.WAIT_TASK: self.wait_task,
            TaskState.STOP_TASK: self.stop_task,
            TaskState.TERM_TASK: self.term_task,
            TaskState.KILL_TASK: self.kill_task,
            TaskState.PUT_LOCAL: self.put_local,
            TaskState.FINAL: self.finalize,
        }

    def start(self: TaskExecutor) -> TaskState:
        """Jump to GET_LOCAL state."""
        log.debug(f'Started (executor-{self.id})')
        return TaskState.GET_LOCAL

    def get_local(self: TaskExecutor) -> TaskState:
        """Get the next task from the local queue of new tasks."""
        try:
            self.task = self.inbound.get(timeout=1)
            self.inbound.task_done()
            return TaskState.CREATE_TASK if self.task else TaskState.FINAL
        except QueueEmpty:
            return TaskState.GET_LOCAL

    def create_task(self: TaskExecutor) -> TaskState:
        """Expand template and initialize task command-line."""
        try:
            self.task.client_id = INSTANCE
            self.task.client_host = HOSTNAME
            self.task.command = self.template.expand(self.task.args)
            return TaskState.START_TASK
        except Exception as error:
            log.error(f'{error.__class__.__name__}: {error}')
            self.task.start_time = datetime.now().astimezone()
            self.task.completion_time = datetime.now().astimezone()
            self.task.exit_status = -1
            return TaskState.PUT_LOCAL

    def start_task(self: TaskExecutor) -> TaskState:
        """Start current task locally."""
        env = task_env(self.task)
        if self.capture:
            self.task.outpath = env['TASK_OUTPATH']
            self.task.errpath = env['TASK_ERRPATH']
            self.redirect_output = open(self.task.outpath, mode='w')
            self.redirect_errors = open(self.task.errpath, mode='w')
        self.task.start_time = datetime.now().astimezone()
        # NOTE: enforce tz aware submit_time (in case of sqlite backend)
        self.task.waited = int((self.task.start_time - self.task.submit_time.astimezone()).total_seconds())
        self.attempted_sigint = False
        self.attempted_sigterm = False
        self.attempted_sigkill = False
        self.process = Popen(self.task.command, shell=True,
                             stdout=self.redirect_output, stderr=self.redirect_errors,
                             cwd=config.task.cwd, env=env)
        log.info(f'Running task ({self.task.id})')
        log.debug(f'Running task ({self.task.id}: {self.task.command})')
        log.trace(f'Running task ({self.task.id}: pid={self.process.pid}, argv={self.task.command})')
        return TaskState.WAIT_TASK

    def wait_task(self: TaskExecutor) -> TaskState:
        """Wait for current task to complete."""
        try:
            self.task.exit_status = self.process.wait(timeout=1)
            self.task.completion_time = datetime.now().astimezone()
            self.task.duration = int((self.task.completion_time - self.task.start_time).total_seconds())
            log.debug(f'Completed task ({self.task.id})')
            if self.capture:
                self.redirect_output.close()
                self.redirect_errors.close()
            return TaskState.PUT_LOCAL
        except TimeoutExpired:
            # Only include time elapsed to the nearest second (we don't need fractions)
            elapsed = timedelta(seconds=round((datetime.now().astimezone() - self.task.start_time).total_seconds()))
            log.trace(f'Waiting on task ({self.task.id}: {elapsed})')
            if self.timeout is None or elapsed.total_seconds() < self.timeout:
                return TaskState.WAIT_TASK
            elif self.attempted_sigint is False:
                log.warning(f'Task exceeded walltime limit ({elapsed})')
                return TaskState.STOP_TASK
            elif self.attempted_sigterm is False:
                log.error(f'Interrupt ignored ({self.task.id})')
                return TaskState.TERM_TASK
            else:
                log.error(f'Terminate ignored ({self.task.id})')
                return TaskState.KILL_TASK

    def stop_task(self: TaskExecutor) -> TaskState:
        """Send SIGINT to task process."""
        log.debug(f'Sending SIGINT ({self.task.id}: {self.process.pid})')
        self.process.send_signal(signal.SIGINT)
        self.attempted_sigint = True
        time.sleep(2)  # additional grace period
        return TaskState.WAIT_TASK

    def term_task(self: TaskExecutor) -> TaskState:
        """Send SIGTERM to task process."""
        log.debug(f'Sending SIGTERM ({self.task.id}: {self.process.pid})')
        self.process.terminate()
        self.attempted_sigterm = True
        time.sleep(2)  # additional grace period
        return TaskState.WAIT_TASK

    def kill_task(self: TaskExecutor) -> TaskState:
        """Send SIGKILL or halt executor if ignored."""
        if self.attempted_sigkill is False:
            log.debug(f'Sending SIGKILL ({self.task.id}: {self.process.pid})')
            self.process.kill()
            self.attempted_sigkill = True
            time.sleep(2)  # additional grace period
            return TaskState.WAIT_TASK
        else:
            log.critical(f'Process ignored SIGKILL ({self.task.id}: {self.process.pid})')
            log.critical(f'Shutting down executor ({self.id})')
            return TaskState.FINAL

    def put_local(self: TaskExecutor) -> TaskState:
        """Put completed task on outbound queue."""
        try:
            self.outbound.put(self.task, timeout=1)
            return TaskState.GET_LOCAL
        except QueueFull:
            return TaskState.PUT_LOCAL

    def finalize(self: TaskExecutor) -> TaskState:
        """Push out any remaining tasks and halt."""
        log.debug(f'Done (executor-{self.id})')
        if self.redirect_output is not sys.stdout:
            self.redirect_output.close()
        if self.redirect_errors is not sys.stderr:
            self.redirect_errors.close()
        return TaskState.HALT


class TaskThread(Thread):
    """Run task executor within dedicated thread."""

    id: int

    def __init__(self: TaskThread,
                 id: int,
                 inbound: Queue[Optional[str]],
                 outbound: Queue[Optional[str]],
                 template: str = DEFAULT_TEMPLATE,
                 capture: bool = False,
                 redirect_output: IO = None,
                 redirect_errors: IO = None,
                 timeout: int = None) -> None:
        """Initialize task executor."""
        self.id = id
        super().__init__(name=f'hypershell-executor-{id}')
        self.machine = TaskExecutor(id=id, inbound=inbound, outbound=outbound, template=template,
                                    redirect_output=redirect_output, redirect_errors=redirect_errors,
                                    capture=capture, timeout=timeout)

    def run_with_exceptions(self: TaskThread) -> None:
        """Run machine."""
        self.machine.run()

    def stop(self: TaskThread, wait: bool = False, timeout: int = None) -> None:
        """Stop machine."""
        log.warning(f'Stopping (executor-{self.id})')
        self.machine.halt()
        super().stop(wait=wait, timeout=timeout)


class HeartbeatState(State, Enum):
    """Finite states for heartbeat machine."""
    START = 0
    SUBMIT = 1
    WAIT = 2
    FINAL = 3
    HALT = 4


DEFAULT_HEARTRATE: int = default.client.heartrate


class ClientHeartbeat(StateMachine):
    """Register heartbeats with remote server."""

    queue: QueueClient
    heartrate: timedelta
    previous: datetime = None

    no_wait: bool = False
    client_state: ClientState = ClientState.RUNNING

    state = HeartbeatState.START
    states = HeartbeatState

    def __init__(self: ClientHeartbeat, queue: QueueClient, heartrate: int = DEFAULT_HEARTRATE) -> None:
        """Initialize heartbeat machine."""
        self.queue = queue
        self.previous = datetime.now()
        self.heartrate = timedelta(seconds=heartrate)

    @functools.cached_property
    def actions(self: ClientHeartbeat) -> Dict[HeartbeatState, Callable[[], HeartbeatState]]:
        return {
            HeartbeatState.START: self.start,
            HeartbeatState.SUBMIT: self.submit,
            HeartbeatState.WAIT: self.wait,
            HeartbeatState.FINAL: self.finalize,
        }

    @staticmethod
    def start() -> HeartbeatState:
        """Jump to SUBMIT state."""
        log.debug(f'Started (heartbeat)')
        return HeartbeatState.SUBMIT

    def submit(self: ClientHeartbeat) -> HeartbeatState:
        """Publish new heartbeat to remote queue."""
        try:
            client_state = self.client_state  # atomic
            heartbeat = Heartbeat.new(state=client_state)
            self.queue.heartbeat.put(heartbeat.pack(), timeout=2)
            if client_state is ClientState.RUNNING:
                log.trace(f'Heartbeat - running ({heartbeat.host}: {heartbeat.uuid})')
                return HeartbeatState.WAIT
            else:
                log.trace(f'Heartbeat - final ({heartbeat.host}: {heartbeat.uuid})')
                return HeartbeatState.FINAL
        except QueueEmpty:
            return HeartbeatState.SUBMIT

    def wait(self: ClientHeartbeat) -> HeartbeatState:
        """Wait until next needed heartbeat."""
        if self.no_wait:
            return HeartbeatState.SUBMIT
        now = datetime.now()
        if (now - self.previous) < self.heartrate:
            time.sleep(1)
            return HeartbeatState.WAIT
        else:
            self.previous = now
            return HeartbeatState.SUBMIT

    @staticmethod
    def finalize() -> HeartbeatState:
        """Stop heartbeats."""
        log.debug(f'Done (heartbeat)')
        return HeartbeatState.HALT


class ClientHeartbeatThread(Thread):
    """Run heartbeat machine within dedicated thread."""

    def __init__(self: ClientHeartbeatThread, queue: QueueClient, heartrate: int = DEFAULT_HEARTRATE) -> None:
        """Initialize heartbeat machine."""
        super().__init__(name=f'hypershell-heartbeat')
        self.machine = ClientHeartbeat(queue=queue, heartrate=heartrate)

    def run_with_exceptions(self: ClientHeartbeatThread) -> None:
        """Run machine."""
        self.machine.run()

    def signal_finished(self: ClientHeartbeatThread) -> None:
        """Set client state to communicate completion."""
        self.machine.client_state = ClientState.FINISHED
        self.machine.no_wait = True

    def stop(self: ClientHeartbeatThread, wait: bool = False, timeout: int = None) -> None:
        """Stop machine."""
        log.warning('Stopping (heartbeat)')
        self.machine.halt()
        super().stop(wait=wait, timeout=timeout)


# Only create one task executor by default
DEFAULT_NUM_TASKS = 1

# We do not delay connecting to the server unless explicitly specified
DEFAULT_DELAY = 0


class ClientThread(Thread):
    """Manage asynchronous task bundle scheduling and receiving."""

    client: QueueClient
    num_tasks: int
    delay_start: float
    no_confirm: bool

    inbound: Queue[Optional[Task]]
    outbound: Queue[Optional[Task]]
    scheduler: ClientSchedulerThread
    collector: ClientCollectorThread
    executors: List[TaskThread]

    def __init__(self: ClientThread,
                 num_tasks: int = DEFAULT_NUM_TASKS,
                 bundlesize: int = DEFAULT_BUNDLESIZE,
                 bundlewait: int = DEFAULT_BUNDLEWAIT,
                 address: Tuple[str, int] = (QueueConfig.host, QueueConfig.port),
                 auth: str = QueueConfig.auth,
                 template: str = DEFAULT_TEMPLATE,
                 redirect_output: IO = None,
                 redirect_errors: IO = None,
                 heartrate: int = DEFAULT_HEARTRATE,
                 capture: bool = False,
                 delay_start: float = DEFAULT_DELAY,
                 no_confirm: bool = False,
                 client_timeout: int = None,
                 task_timeout: int = None) -> None:
        """Initialize queue manager and child threads."""
        super().__init__(name='hypershell-client')
        self.num_tasks = num_tasks
        self.delay_start = delay_start
        self.no_confirm = no_confirm
        self.client = QueueClient(config=QueueConfig(host=address[0], port=address[1], auth=auth))
        self.inbound = Queue(maxsize=bundlesize)
        self.outbound = Queue(maxsize=bundlesize)
        self.scheduler = ClientSchedulerThread(queue=self.client, local=self.inbound,
                                               no_confirm=no_confirm, timeout=client_timeout)
        self.heartbeat = ClientHeartbeatThread(queue=self.client, heartrate=heartrate)
        self.collector = ClientCollectorThread(queue=self.client, local=self.outbound,
                                               bundlesize=bundlesize, bundlewait=bundlewait)
        self.executors = [TaskThread(id=count+1,
                                     inbound=self.inbound, outbound=self.outbound,
                                     redirect_output=redirect_output, redirect_errors=redirect_errors,
                                     template=template, capture=capture, timeout=task_timeout)
                          for count in range(num_tasks)]

    def run_with_exceptions(self: ClientThread) -> None:
        """Start child threads, wait."""
        log.debug(f'Started ({self.num_tasks} executors)')
        self.wait_start()
        with self.client:
            self.start_threads()
            self.wait_scheduler()
            self.wait_executors()
            self.wait_collector()
            self.wait_heartbeat()
        log.debug('Done')

    def wait_start(self: ClientThread) -> None:
        """Wait constant period or random interval."""
        if self.delay_start == 0:
            return
        if self.delay_start > 0:
            log.debug(f'Waiting ({self.delay_start} seconds)')
            time.sleep(self.delay_start)
        else:
            delay = random.uniform(0, -1 * self.delay_start)
            log.debug(f'Waiting random ({delay:.1f} seconds)')
            time.sleep(delay)

    def start_threads(self: ClientThread) -> None:
        """Start child threads."""
        self.scheduler.start()
        self.collector.start()
        self.heartbeat.start()
        for executor in self.executors:
            executor.start()

    def wait_scheduler(self: ClientThread) -> None:
        """Wait for all tasks to be completed."""
        log.trace('Waiting (scheduler)')
        self.scheduler.join()

    def wait_collector(self: ClientThread) -> None:
        """Signal collector to halt."""
        log.trace('Waiting (collector)')
        self.outbound.put(None)
        self.collector.join()

    def wait_executors(self: ClientThread) -> None:
        """Send disconnect signal to each task executor thread."""
        for _ in self.executors:
            self.inbound.put(None)  # signal executors to shut down
        for thread in self.executors:
            log.trace(f'Waiting (executor-{thread.id})')
            thread.join()

    def wait_heartbeat(self: ClientThread) -> None:
        """Signal HALT on heartbeat."""
        log.trace('Waiting (heartbeat)')
        self.heartbeat.signal_finished()
        self.heartbeat.join()

    def stop(self: ClientThread, wait: bool = False, timeout: int = None) -> None:
        """Stop child threads before main thread."""
        log.warning('Stopping')
        self.scheduler.stop(wait=wait, timeout=timeout)
        self.collector.stop(wait=wait, timeout=timeout)
        super().stop(wait=wait, timeout=timeout)


def run_client(num_tasks: int = DEFAULT_NUM_TASKS,
               bundlesize: int = DEFAULT_BUNDLESIZE, bundlewait: int = DEFAULT_BUNDLEWAIT,
               address: Tuple[str, int] = (QueueConfig.host, QueueConfig.port), auth: str = QueueConfig.auth,
               template: str = DEFAULT_TEMPLATE, redirect_output: IO = None, redirect_errors: IO = None,
               capture: bool = False, heartrate: int = DEFAULT_HEARTRATE,
               delay_start: float = DEFAULT_DELAY, no_confirm: bool = False,
               client_timeout: int = None, task_timeout: int = None) -> None:
    """Run client until disconnect signal received."""
    thread = ClientThread.new(num_tasks=num_tasks, bundlesize=bundlesize, bundlewait=bundlewait,
                              address=address, auth=auth, template=template, capture=capture,
                              redirect_output=redirect_output, redirect_errors=redirect_errors,
                              heartrate=heartrate, delay_start=delay_start, no_confirm=no_confirm,
                              client_timeout=client_timeout, task_timeout=task_timeout)
    try:
        thread.join()
    except Exception:
        thread.stop()
        raise


APP_NAME = 'hyper-shell client'
APP_USAGE = f"""\
Usage:
hyper-shell client [-h] [-N NUM] [-t CMD] [-b SIZE] [-w SEC] [-H ADDR] [-p PORT]
                   [-k KEY] [--capture | [-o PATH] [-e PATH]] [--no-confirm]
                   [--delay-start SEC] [--timeout SEC] [--task-timeout SEC]

Launch client directly, run tasks in parallel.\
"""

APP_HELP = f"""\
{APP_USAGE}

Tasks are pulled off of the shared queue in bundles from the server and run
locally within the same shell as the client. By default the bundle size is one,
meaning that at small scales there is greater responsiveness. It is recommended
to coordinate these parameters to be the same as the server.

Options:
  -N, --num-tasks     NUM   Number of tasks to run in parallel (default: {DEFAULT_NUM_TASKS}).
  -t, --template      CMD   Command-line template pattern (default: "{DEFAULT_TEMPLATE}").
  -b, --bundlesize    SIZE  Bundle size for finished tasks (default: {DEFAULT_BUNDLESIZE}).
  -w, --bundlewait    SEC   Seconds to wait before flushing tasks (default: {DEFAULT_BUNDLEWAIT}).
  -H, --host          ADDR  Hostname for server.
  -p, --port          NUM   Port number for server.
  -k, --auth          KEY   Cryptographic key to connect to server.
  -d, --delay-start   SEC   Seconds to wait before start-up (default: {DEFAULT_DELAY}).
      --no-confirm          Disable confirmation of task bundle received.
  -o, --output        PATH  Redirect task output (default: <stdout>).
  -e, --errors        PATH  Redirect task errors (default: <stderr>).
  -c, --capture             Capture individual task <stdout> and <stderr>.
  -T, --timeout       SEC   Automatically shutdown if no tasks received (default: never).
  -W, --task-timeout  SEC   Task-level walltime limit (default: none).
  -h, --help                Show this message and exit.\
"""


class ClientApp(Application):
    """Run individual client directly."""

    name = APP_NAME
    interface = Interface(APP_NAME,
                          colorize_usage(APP_USAGE),
                          colorize_usage(APP_HELP))

    num_tasks: int = DEFAULT_NUM_TASKS
    interface.add_argument('-N', '--num-tasks', type=int, default=num_tasks)

    host: str = config.server.bind
    interface.add_argument('-H', '--host', default=host)

    port: int = config.server.port
    interface.add_argument('-p', '--port', type=int, default=port)

    auth: str = config.server.auth
    interface.add_argument('-k', '--auth', default=auth)

    template: str = DEFAULT_TEMPLATE
    interface.add_argument('-t', '--template', default=template)

    bundlesize: int = config.submit.bundlesize
    interface.add_argument('-b', '--bundlesize', type=int, default=bundlesize)

    bundlewait: int = config.submit.bundlewait
    interface.add_argument('-w', '--bundlewait', type=int, default=bundlewait)

    delay_start: float = DEFAULT_DELAY
    interface.add_argument('-d', '--delay-start', type=float, default=delay_start)

    task_timeout: int = config.task.timeout
    client_timeout: int = config.client.timeout
    interface.add_argument('-T', '--timeout', type=int, default=client_timeout, dest='client_timeout')
    interface.add_argument('-W', '--task-timeout', type=int, default=task_timeout, dest='task_timeout')

    no_confirm: bool = False
    interface.add_argument('--no-confirm', action='store_true')

    output_path: str = None
    errors_path: str = None
    interface.add_argument('-o', '--output', default=None, dest='output_path')
    interface.add_argument('-e', '--errors', default=None, dest='errors_path')

    capture: bool = False
    interface.add_argument('-c', '--capture', action='store_true')

    exceptions = {
        EOFError: functools.partial(handle_disconnect, logger=log),
        ConnectionResetError: functools.partial(handle_disconnect, logger=log),
        ConnectionRefusedError: functools.partial(handle_exception, logger=log, status=exit_status.runtime_error),
        AuthenticationError: functools.partial(handle_exception, logger=log, status=exit_status.runtime_error),
        HostAddressInfo: functools.partial(handle_address_unknown, logger=log, status=exit_status.runtime_error),
        **get_shared_exception_mapping(__name__),
    }

    def run(self: ClientApp) -> None:
        """Run client."""
        try:
            self.check_args()
            run_client(num_tasks=self.num_tasks,
                       bundlesize=self.bundlesize,
                       bundlewait=self.bundlewait,
                       address=(self.host, self.port),
                       auth=self.auth,
                       template=self.template,
                       redirect_output=self.output_stream,
                       redirect_errors=self.errors_stream,
                       capture=self.capture,
                       delay_start=self.delay_start,
                       no_confirm=self.no_confirm,
                       heartrate=config.client.heartrate,
                       client_timeout=self.client_timeout,
                       task_timeout=self.task_timeout)
        except gaierror:
            raise HostAddressInfo(f'Could not resolve host \'{self.host}\'')

    def check_args(self: ClientApp) -> None:
        """Check for logical errors in command-line arguments."""
        if self.capture and (self.output_path or self.errors_path):
            raise ArgumentError('Cannot specify --capture with either --output or --errors')
        if self.client_timeout is not None and self.client_timeout <= 0:
            raise ArgumentError('Client --timeout should be positive integer')
        if self.task_timeout is not None and self.task_timeout <= 0:
            raise ArgumentError('Client --task-timeout should be positive integer')

    @functools.cached_property
    def output_stream(self: ClientApp) -> IO:
        """IO stream for task outputs."""
        return sys.stdout if not self.output_path else open(self.output_path, mode='w')

    @functools.cached_property
    def errors_stream(self: ClientApp) -> IO:
        """IO stream for task errors."""
        return sys.stderr if not self.errors_path else open(self.errors_path, mode='w')

    def __exit__(self: ClientApp,
                 exc_type: Optional[Type[Exception]],
                 exc_val: Optional[Exception],
                 exc_tb: Optional[TracebackType]) -> None:
        """Close IO streams if necessary."""
        if self.output_stream is not sys.stdout:
            self.output_stream.close()
        if self.errors_stream is not sys.stderr:
            self.errors_stream.close()
