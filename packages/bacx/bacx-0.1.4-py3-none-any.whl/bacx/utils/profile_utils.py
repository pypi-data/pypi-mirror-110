import logging
import time

logger = logging.getLogger(__name__)
_TIME_MAP = {}
_COUNT_MAP = {}


def timer_start(key: str) -> None:
    """
    Start a named timer with name `key`.
    For each timer we are counting
    - the total running time
    - number of measurements
    """
    if key not in _TIME_MAP:
        _TIME_MAP[key] = 0
    if key not in _COUNT_MAP:
        _COUNT_MAP[key] = 0
    _TIME_MAP[key] -= time.perf_counter()


def timer_stop(key: str) -> None:
    """
    Stop/pause the timer with name `key`
    """
    _TIME_MAP[key] += time.perf_counter()
    _COUNT_MAP[key] += 1


def timer_reset(*keys: str, clear: bool = False) -> None:
    """
    Reset all timers or just timers with keys in `keys` back to zero.
    """
    if clear:
        _TIME_MAP.clear()
        _COUNT_MAP.clear()
    if not keys:
        logger.info(f"RESET ALL TIMERS")
        keys = _TIME_MAP.keys()
    else:
        logger.info(f"RESET TIMERS: {keys or ''}")
        "__reset__" in _TIME_MAP and timer_stop("__reset__")
    for key in keys:
        _TIME_MAP[key] = 0
        _COUNT_MAP[key] = 0
    timer_start("__reset__")


def timer_log(*keys: str) -> None:
    """
    Print statistics for each key in `keys` (or all keys).
    For each key we print total consumed time and average time per measurement
    """
    "__reset__" in _TIME_MAP and timer_stop("__reset__")
    if not keys:
        logger.info(f"STATS FOR ALL TIMERS")
        keys = _TIME_MAP.keys()
    else:
        logger.info(f"TIMERS STATS FOR: {' '.join(keys)}")
    for key in keys:
        value = _TIME_MAP[key] if _TIME_MAP[key] >= 0 else -1
        average = value / _COUNT_MAP[key] if _COUNT_MAP[key] > 0 else 0
        logger.info(f"    {key:10}: {value:8.3f}s   ({average:.6f}s)")


def timer_get_stats(*keys: str) -> dict:
    """
    Return profile statistics as dictionary
    """
    "__reset__" in _TIME_MAP and timer_stop("__reset__")
    if not keys:
        keys = _TIME_MAP.keys()
    result = {key: (_TIME_MAP[key], _COUNT_MAP[key]) for key in keys}
    "__reset__" in _TIME_MAP and timer_start("__reset__")
    return result


if __name__ == "__main__":  # pragma: no cover
    """Usage example."""
    logging.basicConfig(level=logging.INFO)

    def foo():
        timer_start("foo")
        time.sleep(0.0001)
        timer_stop("foo")
        timer_start("bar")
        timer_stop("bar")

    for _ in range(1000):
        foo()
    timer_log("foo")
    timer_log()

    timer_reset()
    for _ in range(1000):
        foo()
    timer_log()
