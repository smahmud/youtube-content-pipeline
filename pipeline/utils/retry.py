"""
Retry utilities for resilient execution in the content-pipeline project.

Provides decorators and helper functions to automatically retry transient operations
such as network requests, file I/O, or subprocess calls with exponential backoff.
Designed for modular use across extractors, transcription, and enrichment stages.
"""
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
                    

