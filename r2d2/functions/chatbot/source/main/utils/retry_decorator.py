import logging
import time
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


def retry(times: int, delay: int, exceptions: tuple[type[Exception], ...], raise_after: bool = True) -> Callable:
    """
    Retry Decorator.
    Retries the function call if the given exceptions are raised.

    :param times: The number of times to retry the function call.
    :param delay: The delay between the retries.
    :param exceptions: The exceptions to catch.
    :param raise_after: If True, the function will raise the exception after the given number of attempts. Default: True

    :return: The wrapped function.
    """

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def wrapped_function(*args, **kwargs) -> Callable:
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempt += 1
                    logger.warning(f'Attempt {attempt} failed. Retrying...')
                    time.sleep(delay)

            return func(*args, **kwargs) if raise_after else None

        return wrapped_function

    return wrapper
