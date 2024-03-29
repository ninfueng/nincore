import time


def second_ddhhmmss(second: int | float) -> str:
    """Convert seconds to days:hours:minute:seconds format.

    Arguments:
        second: a time in second.

    Returns:
        run_time: a converted time in dd:hh:mm:ss format.
    """
    days = int(second // (60 * 60 * 24))
    runtime = time.strftime('%H:%M:%S', time.gmtime(second))
    runtime = f'{days:02d}:' + runtime
    return runtime


if __name__ == '__main__':
    t0 = time.perf_counter()
    time.sleep(1)
    t1 = time.perf_counter()
    diff = t1 - t0
    print(diff)

    # Number of second of a day: 86_400 = 60 * 60 * 24
    seconds = 86_400 * 101
    time_format = second_ddhhmmss(seconds)
    print(time_format)

    seconds = 86_400 * 1.5
    time_format = second_ddhhmmss(seconds)
    print(time_format)
