from typing import Protocol
from typing import TYPE_CHECKING
from abc import abstractmethod

if TYPE_CHECKING:
    from indecro.api.job import Job


class Executor(Protocol):
    if TYPE_CHECKING:
        @abstractmethod
        async def execute(self, job: Job) -> bool:
            raise NotImplementedError()
