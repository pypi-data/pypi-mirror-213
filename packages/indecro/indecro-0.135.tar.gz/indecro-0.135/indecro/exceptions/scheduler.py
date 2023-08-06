from typing import TYPE_CHECKING

from indecro.api.job import Job
from indecro.exceptions.base import IndecroException


# root exception, bounded to scheduler work
class SchedulerException(IndecroException):
    if TYPE_CHECKING:
        def __init__(self, job: Job):
            self.job = job
