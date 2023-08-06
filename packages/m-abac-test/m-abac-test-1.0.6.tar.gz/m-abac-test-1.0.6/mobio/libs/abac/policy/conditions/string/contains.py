"""
    String contains conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class Contains(StringCondition):
    """
        Condition for string `self.what` contains `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if self.case_insensitive:
                    if i.lower() in self.what.lower():
                        return True
                else:
                    if i in self.what:
                        return True
            return False
        else:
            for i in self.values:
                if self.case_insensitive:
                    if i.lower() not in self.what.lower():
                        return False
                else:
                    if i not in self.what:
                        return False
            return True

class ContainsSchema(StringConditionSchema):
    """
        JSON schema for contains string conditions
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Contains(**data)
