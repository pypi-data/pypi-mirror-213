"""Exceptions used in this module."""


class AwsEcsExecException(Exception):
    """Base exception class for all custom exceptions."""


class UserDeclined(AwsEcsExecException):
    """The user declined a query."""


class NoChoices(AwsEcsExecException):
    """There are no choices."""
