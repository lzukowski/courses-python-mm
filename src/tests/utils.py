from contextlib import contextmanager
from functools import wraps
from typing import Callable, Text, Type

from dev_droga_courses.shared.service import Result, successful


def succeeded(result: Result) -> None:
    if not successful(result):
        failure = result.failure()
        raise (
            failure
            if isinstance(failure, Exception)
            else AssertionError(failure)
        )


def failed(result: Result, expected: Type[Exception]) -> None:
    if successful(result):
        raise AssertionError(result.unwrap())

    if not isinstance(result.failure(), expected):
        raise result.failure()


def raises(exception: Exception) -> Callable:
    def _wrap_test(test):
        @wraps(test)
        def _execute_call(*args, **kwargs):
            try:
                test(*args, **kwargs)
                assert False, f'Did not raise {exception}'
            except exception:
                pass
        return _execute_call
    return _wrap_test


@contextmanager
def step(name: Text):
    yield name


given = step
when = step
then = step
expect = step
