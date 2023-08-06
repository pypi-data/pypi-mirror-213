import asyncio
from abc import abstractmethod
from dataclasses import dataclass, is_dataclass
from datetime import datetime
from typing import Optional, Any, Union

from indecro.api.executor import Executor
from indecro.api.task import Task
from indecro.api.rules import Rule, BoolRule
from indecro.api.scheduler import Scheduler
from indecro.api.job import Job as JobProtocol, RunAs


@dataclass
class Job(JobProtocol):  # If the Job is highlighted in red, the bad work of the paycharm with dataclasses and
    # typehints for them is to blame
    task: Task
    rule: Union[Rule, BoolRule]

    next_run_time: datetime

    daemonize: RunAs = RunAs.FUNCTION

    id: Optional[str] = None

    is_running: bool = False

    scheduler: Optional[Scheduler] = None
    executor: Optional[Executor] = None

    running_task: Optional[asyncio.Task] = None

    def schedule(self) -> None:
        if self.scheduler is None:
            raise ValueError('To use schedule shortcut you must provide an scheduler attribute for job object')

        self.scheduler.schedule_job(self)

    async def execute(self, reschedule: bool = True) -> bool:
        if self.executor is None:
            raise ValueError('To use execute shortcut you must provide an executor attribute for job object')

        executed = await self.executor.execute(self)

        if reschedule:
            self.schedule()

        return executed

    def __hash__(self):
        return hash(hash(self.rule) + hash(self.id) + hash(self.task))
