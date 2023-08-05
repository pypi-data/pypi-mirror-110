"""fuzzy duration package."""

import sys

__version__ = "0.2.0"


def pluralise(val, label):
    try:
        if val == 1:
            return label
        return f"{label}s"
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def fuzzyDuration(seconds):
    try:
        divisors = [60, 60, 24, 7, 52, 1]
        units = ["second", "minute", "hour", "day", "week", "year"]
        for i in range(len(divisors)):
            result = seconds / divisors[i]
            if result < 1:
                break
            else:
                seconds = int(result)
        return f"{seconds} {pluralise(seconds, units[i])}"
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
