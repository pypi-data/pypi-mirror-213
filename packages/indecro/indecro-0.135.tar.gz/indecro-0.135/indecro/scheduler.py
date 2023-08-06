import asyncio
import functools
from datetime import datetime
from typing import Optional, Union, Awaitable

from indecro.api.executor import Executor
from indecro.api.job import RunAs
from indecro.api.task import Task
from indecro.api.job import Job as JobProtocol
from indecro.api.rules import Rule
from indecro.api.scheduler import Scheduler as SchedulerProtocol
from indecro.api.storage import Storage, AsyncStorage

from indecro.defaults import SECONDS_PER_LOOP
from indecro.exceptions.rule import JobNeverBeScheduled, CannotPredictJobSchedulingTime

from indecro.job import Job


class Scheduler(SchedulerProtocol):
    def __init__(
            self,
            storage: Union[Storage, AsyncStorage],
            executor: Executor,
            loop_delay: Union[int, float] = SECONDS_PER_LOOP
    ):
        self.storage = storage
        self.executor = executor

        self.loop_delay = loop_delay

        self.running = False

    def job(
            self,
            rule: Rule,

            daemonize: RunAs = RunAs.FUNCTION,

            id: Optional[str] = None,

            *args,
            **kwargs
    ):
        def decorator(task: Task):
            self.add_job(
                task=task,
                rule=rule,
                daemonize=daemonize,
                id=id,
                *args,
                **kwargs
            )
            return task

        return decorator

    def add_job(
            self,
            task: Task,
            rule: Rule,

            daemonize: RunAs = RunAs.FUNCTION,

            id: Optional[str] = None,
            *args,
            **kwargs
    ) -> JobProtocol:
        if isinstance(task, Job):
            job = task
        else:
            try:
                next_run_time = rule.get_next_schedule_time(after=datetime.now())
            except CannotPredictJobSchedulingTime:
                next_run_time = None
            job = Job(
                task=functools.partial(task, *args, **kwargs),
                rule=rule,
                next_run_time=next_run_time,
                id=id,
                scheduler=self,
                executor=self.executor,
                daemonize=daemonize
            )

        return self.storage.add_job(job)

    def stop(self):
        self.running = False

    async def execute_job(self, job: Union[JobProtocol, str], reschedule: bool = True) -> bool:
        if isinstance(job, str):
            job = self.storage.get_job(job)
            if job is None:
                raise

        return await job.execute(reschedule=reschedule)

    def schedule_job(self, job: Union[JobProtocol, str]):
        if isinstance(job, str):
            job = self.storage.get_job(job)
            if job is None:
                raise

        try:
            job.next_run_time = job.rule.get_next_schedule_time(after=datetime.now())
        except CannotPredictJobSchedulingTime:
            pass

    def remove_job(self, job: Union[JobProtocol, str]):
        if isinstance(job, str):
            job = self.storage.get_job(job)
            if job is None:
                raise

        return self.storage.remove_job(job)

    async def run(self):
        self.running = True
        while self.running:
            now = datetime.now()

            any_job_started = False
            for job in self.storage.iter_actual_jobs(before=now):
                job_executed = False  # Setting a default value

                try:
                    job_executed = await self.execute_job(job)
                except JobNeverBeScheduled:
                    res = self.storage.remove_job(job)

                    if isinstance(res, Awaitable):
                        await res
                except CannotPredictJobSchedulingTime:  # Looks like BoolRule, we just wait
                    pass

                any_job_started = job_executed or any_job_started

            # Sleeping loop_delay seconds if not any job started, else sleeping 0 seconds (asyncio magic)
            await asyncio.sleep(self.loop_delay * (not any_job_started))
