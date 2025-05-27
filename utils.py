# utils.py

import time
import functools

def retry(times=3, delay=1.0):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < times - 1:
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator_retry
