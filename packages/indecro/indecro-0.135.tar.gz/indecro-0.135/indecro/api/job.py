import asyncio
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Protocol, Union

from indecro.api.executor import Executor
from indecro.api.rules import Rule, BoolRule
from indecro.api.scheduler import Scheduler
from indecro.api.task import Task


class RunAs(Enum):
    FUNCTION = 'FUNCTION'
    ASYNC_TASK = 'ASYNC_TASK'
    THREAD = 'THREAD'


@dataclass
class Job(Protocol):
    task: Task
    rule: Union[Rule, BoolRule]

    next_run_time: datetime

    daemonize: RunAs = RunAs.FUNCTION

    id: Optional[str] = None

    is_running: bool = False

    scheduler: Optional[Scheduler] = None
    executor: Optional[Executor] = None

    running_task: Optional[asyncio.Task] = None

    @abstractmethod
    def schedule(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def execute(self, reschedule: bool = True) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError()
