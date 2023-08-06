from abc import abstractmethod
from asyncio import Protocol
from datetime import datetime, timedelta

from typing import NoReturn, Union, Optional


class Rule(Protocol):
    @abstractmethod
    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        raise NotImplementedError()

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError()

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError()


class CheckEvery:
    def __init__(
            self,
            time: Optional[Union[timedelta, int, float]] = None,
            iteration: Optional[int] = None,
            seconds_per_iteration: Optional[Union[int, float]] = None
    ):
        if time is None and (iteration is None or seconds_per_iteration is None):
            raise ValueError('You must provide time parameter or iteration and seconds_per_iteration parameters')

        if time is not None and (iteration is not None or seconds_per_iteration is not None):
            raise ValueError('You must choice only one variant: provide time parameter or iteration and '
                             'seconds_per_iteration parameters')

        if sum(map(bool, [iteration, seconds_per_iteration])):  # xor
            raise ValueError('If you provide first argument for iteration-based time calculating, you must provide '
                             'second argument for iteration-based time calculating')

        if time is None:
            iteration: Union[int, float]
            seconds_per_iteration: Union[int, float]
            time = iteration * seconds_per_iteration

        if isinstance(time, (int, float)):
            time = timedelta(seconds=time)

        self._check_period = time

        self.last_check_time = datetime.now()
        self.next_check_time = self.get_next_check_time(self.last_check_time)

    def get_next_check_time(self, after: datetime) -> datetime:
        next_check_time = self.last_check_time

        while True:
            next_check_time += self.check_period
            if next_check_time > after:
                self.next_check_time = next_check_time
                return next_check_time

    @property
    def check_period(self) -> timedelta:
        return self._check_period


class BoolRule(Rule, Protocol):
    def __init__(self, check_every: CheckEvery):
        self.check_every = check_every

    @abstractmethod
    def get_must_be_scheduled_now_flag(self) -> bool:
        raise NotImplementedError()

    def get_next_schedule_time(self, *, after: datetime) -> NoReturn:
        from indecro.exceptions.rule import CannotPredictJobSchedulingTime

        raise CannotPredictJobSchedulingTime(after=after, by_rule=self)
