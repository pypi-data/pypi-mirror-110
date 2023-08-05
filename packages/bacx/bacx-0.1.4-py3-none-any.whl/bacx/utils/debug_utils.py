import logging


def tee_log(value):
    """
    Log value and pass it as result. (T shaped pipe). Saves space as you don't need store the result before using it.

    Example usages:
    - `return tee_log(a + b + c)`
    - `foo(tee_log(bar(...)))`
    """
    logging.info(value)
    return value
