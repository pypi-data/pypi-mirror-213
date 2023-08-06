from abc import abstractmethod
from datetime import datetime
from typing import Protocol, Generator, AsyncGenerator, Optional, Union

from indecro.api.job import Job


class Storage(Protocol):
    @abstractmethod
    def add_job(self, job: Union[Job, str]) -> Job:
        raise NotImplementedError()

    @abstractmethod
    def remove_job(self, job: Union[Job, str]):
        raise NotImplementedError()

    @abstractmethod
    def get_job(self, job_id: str) -> Job:
        raise NotImplementedError()

    @abstractmethod
    def get_closest_job(self, *, after: datetime) -> Union[Job, None]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def next_job(self) -> Union[Job, None]:
        raise NotImplementedError()

    @abstractmethod
    def get_duty_job(self, *, before: datetime) -> Union[Job, None]:
        for job in self.iter_actual_jobs(before=before):
            return job
        return None

    @property
    @abstractmethod
    def duty_job(self) -> Union[Job, None]:
        return self.get_duty_job(before=datetime.now())

    @abstractmethod
    def iter_actual_jobs(
            self,
            *,
            after: Optional[datetime] = None,
            before: Optional[datetime] = None,
            limit: Optional[int] = None
    ) -> Generator[Job, None, None]:
        raise NotImplementedError()


class AsyncStorage(Protocol):
    @abstractmethod
    async def add_job(self, job: Union[Job, str]) -> Job:
        raise NotImplementedError()

    @abstractmethod
    async def remove_job(self, job: Union[Job, str]):
        raise NotImplementedError()

    @abstractmethod
    async def get_closest_job(self, *, after: datetime) -> Union[Job, None]:
        raise NotImplementedError()

    @abstractmethod
    async def get_duty_job(self, *, before: datetime) -> Union[Job, None]:
        raise NotImplementedError()

    @property
    @abstractmethod
    async def duty_job(self) -> Union[Job, None]:
        raise NotImplementedError()

    @property
    @abstractmethod
    async def next_job(self) -> Union[Job, None]:
        raise NotImplementedError()

    @abstractmethod
    async def iter_actual_jobs(
            self,
            *,
            after: Optional[datetime] = None,
            before: Optional[datetime] = None,
            limit: Optional[int] = None
    ) -> AsyncGenerator[Job, None]:
        raise NotImplementedError()
        yield  # For generator-like typehints in PyCharm

    @abstractmethod
    def __iter__(self) -> Generator[Job, None, None]:
        raise NotImplementedError()
