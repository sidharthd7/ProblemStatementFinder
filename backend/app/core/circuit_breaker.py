from functools import wraps
import time
from typing import Callable, Any
import logging
from ...core.metrics import track_request_metrics

logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: int = 60,
        expected_exception: tuple = (Exception,)
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = 0
        self.is_open = False

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if self.is_open:
                if time.time() - self.last_failure_time >= self.reset_timeout:
                    logger.info("Circuit breaker reset timeout reached, attempting to close")
                    self.is_open = False
                    self.failure_count = 0
                else:
                    logger.warning("Circuit breaker is open, request rejected")
                    raise Exception("Circuit breaker is open")

            try:
                result = await func(*args, **kwargs)
                self.failure_count = 0
                return result
            except self.expected_exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.is_open = True
                    logger.error(f"Circuit breaker opened after {self.failure_count} failures")
                
                raise e

        return wrapper

def circuit_breaker(
    failure_threshold: int = 5,
    reset_timeout: int = 60,
    expected_exception: tuple = (Exception,)
):
    """
    Decorator for implementing circuit breaker pattern
    """
    def decorator(func: Callable) -> Callable:
        breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            reset_timeout=reset_timeout,
            expected_exception=expected_exception
        )
        return breaker(func)
    return decorator

# Example usage:
# @circuit_breaker(failure_threshold=3, reset_timeout=30)
# async def call_external_service():
#     # Your external service call here
#     pass 