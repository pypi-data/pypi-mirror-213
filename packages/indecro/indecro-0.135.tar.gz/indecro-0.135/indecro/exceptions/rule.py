from datetime import datetime

from indecro.api.rules import Rule
from indecro.exceptions.base import IndecroException


# root exception, bounded to rule
class RuleException(IndecroException):
    def __init__(self, rule: Rule):
        self.rule = rule

        super().__init__()


# Cannot do smth bounded with rule
class RuleCannotSmthException(RuleException):
    def __init__(self, *, after: datetime, by_rule: Rule):
        super().__init__(rule=by_rule)

        self.after = after
        self.by_rule = by_rule

    def __repr__(self):
        return f'{self.__class__.__name__}(after={self.after}, by_rule={self.by_rule})'


# At main, for BoolRule
class CannotPredictJobSchedulingTime(RuleCannotSmthException):
    pass


# For SingleRun and other similar rules
class JobNeverBeScheduled(RuleCannotSmthException):
    pass
