from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Callable, Any, Union

from magic_filter import MagicFilter

from indecro.api.rules import Rule, BoolRule, CheckEvery

from indecro.defaults import SECONDS_PER_LOOP
from indecro.exceptions.rule import JobNeverBeScheduled


@dataclass
class RunEvery(Rule):
    period: timedelta
    after: Optional[Union[datetime, timedelta]] = None
    before: Optional[Union[datetime, timedelta]] = None
    repeat: Optional[int] = None

    init_time: datetime = field(default_factory=datetime.now)

    repeats: int = 0

    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        # Lazy after timedelta to datetime transformation instead of __init__ redefinition
        if isinstance(self.after, timedelta):
            self.after = self.init_time + self.after

        # similar actions for before
        if isinstance(self.before, timedelta):
            self.before = self.init_time + self.before

        delta = after - self.init_time
        intervals = delta.total_seconds() // self.period.total_seconds() + 1

        next_schedule_time = self.init_time + intervals * self.period

        if self.before is not None and self.before <= next_schedule_time:
            raise JobNeverBeScheduled(after=after, by_rule=self)

        if self.repeat is not None and self.repeat <= self.repeats:
            raise JobNeverBeScheduled(after=after, by_rule=self)

        if self.after is not None and self.after > next_schedule_time:
            next_schedule_time = self.after
            self.after = None

        self.repeats += 1

        return next_schedule_time

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(start={repr(self.after)}, period={repr(self.period)})'

    def __hash__(self):
        return hash(repr(self))


# Execute job just one time
@dataclass(init=False)
class RunOnce(Rule):
    at: Optional[datetime] = None
    # time_to_execute = at
    after: Optional[timedelta] = None

    # time_to_execute = now + after

    def __init__(
            self,
            at: Optional[datetime] = None,
            after: Optional[timedelta] = None
    ):
        if (not at) and (not after):
            raise ValueError('You must provide at parameter or after parameter')

        if at is None:
            at = datetime.now() + after

        self.at = at
        self.after = after

    def get_next_schedule_time(self, *, after: datetime) -> datetime:
        if after > self.at:
            raise JobNeverBeScheduled(after=after, by_rule=self)
        return self.at

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(at={repr(self.at)}, after={self.after})'

    def __hash__(self):
        return hash(repr(self))


# The most useful BoolRule realisation example
@dataclass
class RunWhen(BoolRule):
    will: Union[MagicFilter, Callable[[], bool]]
    subject: Union[None, Any] = None

    repeats: int = -1

    check_every: CheckEvery = CheckEvery(timedelta(seconds=SECONDS_PER_LOOP))

    repeats_passed: int = 0

    def get_must_be_scheduled_now_flag(self):
        if isinstance(self.will, MagicFilter):
            res = self.will.resolve(self.subject)
        elif isinstance(self.will, Callable):
            res = self.will()
        else:
            res = False

        if res is True:
            self.repeats_passed += 1

        if self.repeats >= 0 and self.repeats_passed > self.repeats:  # PyCharm, fuck you
            raise JobNeverBeScheduled(after=datetime.now(), by_rule=self)
        return res

    def __repr__(self):
        # TODO: Remove hardcode from arguments displaying in repr
        return f'{self.__class__.__name__}(at={repr(self.will)}, after={self.subject})'

    def __hash__(self):
        return hash(repr(self))
