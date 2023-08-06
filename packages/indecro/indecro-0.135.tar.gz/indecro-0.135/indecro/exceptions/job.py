from dataclasses import dataclass

from indecro.exceptions.base import IndecroException


class JobException(IndecroException):
    pass


@dataclass
class JobNotFound(JobException):
    by_id: str
