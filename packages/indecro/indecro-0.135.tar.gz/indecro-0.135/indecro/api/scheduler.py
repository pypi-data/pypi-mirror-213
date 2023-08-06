from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Optional, Union, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from indecro.api.job import RunAs
    from indecro.api.job import Job

from indecro.api.task import Task
from indecro.api.rules import Rule


class Scheduler(Protocol):
    if TYPE_CHECKING:
        @abstractmethod
        def job(
                self,
                rule: Rule,

                daemonize: RunAs = RunAs.FUNCTION,

                id: Optional[str] = None,

                *args,
                **kwargs
        ):
            raise NotImplementedError()

        @abstractmethod
        def add_job(
                self,
                task: Task,
                rule: Rule,

                daemonize: RunAs = RunAs.FUNCTION,

                id: Optional[str] = None,

                *args,
                **kwargs
        ) -> Union[Job, Awaitable[Job]]:
            raise NotImplementedError()

        @abstractmethod
        async def execute_job(self, job: Union[Job, str], reschedule: bool = True):
            raise NotImplementedError()

        @abstractmethod
        def schedule_job(self, job: Union[Job, str]):
            raise NotImplementedError()

        @abstractmethod
        def remove_job(self, job: Union[Job, str]):
            pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    async def run(self):
        raise NotImplementedError()
