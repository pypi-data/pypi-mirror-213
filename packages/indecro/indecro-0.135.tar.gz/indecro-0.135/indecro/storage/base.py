from abc import ABC, abstractmethod
from datetime import datetime

from typing import Generator, AsyncGenerator, Optional, Union

from indecro.api.job import Job
from indecro.api.storage import Storage, AsyncStorage
from indecro.exceptions.job import JobNotFound


class BaseStorage(Storage, ABC):
    def get_closest_job(self, *, after: datetime) -> Union[Job, None]:
        for job in self.iter_actual_jobs(after=after):
            return job
        return None

    def get_duty_job(self, *, before: datetime) -> Union[Job, None]:
        for job in self.iter_actual_jobs(before=before):
            return job
        return None

    def get_job(self, job_id: str) -> Job:
        for job in self:
            if job.id == job_id:
                return job
        raise JobNotFound(by_id=job_id)

    @property
    def duty_job(self) -> Union[Job, None]:
        return self.get_duty_job(before=datetime.now())

    @property
    def next_job(self) -> Union[Job, None]:
        return self.get_closest_job(after=datetime.now())

    @abstractmethod
    def iter_actual_jobs(
            self,
            *,
            after: Optional[datetime] = None,
            before: Optional[datetime] = None,
            limit: Optional[int] = None
    ) -> Generator[Job, None, None]:
        raise NotImplementedError()

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()


class BaseAsyncStorage(AsyncStorage, ABC):
    async def get_closest_job(self, *, after: datetime) -> Union[Job, None]:
        async for job in self.iter_actual_jobs(after=after):
            return job
        return None

    async def get_duty_job(self, *, before: datetime) -> Union[Job, None]:
        async for job in self.iter_actual_jobs(before=before):
            return job
        return None

    @property
    async def duty_job(self) -> Union[Job, None]:
        return await self.get_duty_job(before=datetime.now())

    @property
    async def next_job(self) -> Union[Job, None]:
        return await self.get_closest_job(after=datetime.now())

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

    async def get_job(self, job_id: str) -> Job:
        async for job in self:
            if job.id == job_id:
                return job
        return None

    @abstractmethod
    async def __aiter__(self):
        raise NotImplementedError()


__all__ = ('BaseStorage', 'BaseAsyncStorage')
