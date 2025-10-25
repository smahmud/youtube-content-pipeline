import time
import logging
from functools import wraps

def retry(max_attempts=3, delay=2, backoff=2):
    """
    Decorator to retry a function on exception
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            wait = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(f"Attempt {attempts} failed: {e}")
                    if attempts < max_attempts:
                        time.sleep(wait)
                        wait *= backoff
                    else:
                        logging.error(f"All {max_attempts} attempts failed.")
                        raise
        return wrapper
    return decorator
                    

