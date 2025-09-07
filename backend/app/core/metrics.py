# backend/app/core/metrics.py
from functools import wraps

# Dummy decorators that do nothing
def track_request_metrics(func):
    return func

def track_db_operation(operation_type, table):
    def decorator(func):
        return func
    return decorator

# Dummy metrics
class DummyMetric:
    def labels(self, **kwargs):
        return self
    def inc(self):
        pass
    def observe(self, value):
        pass
    def _value(self):
        return {"get": lambda: 0}

REQUEST_COUNT = DummyMetric()
REQUEST_LATENCY = DummyMetric()
DB_OPERATION_COUNT = DummyMetric()
DB_OPERATION_LATENCY = DummyMetric()
ACTIVE_USERS = DummyMetric()


# from prometheus_client import Counter, Histogram, Gauge
# from functools import wraps
# import time

# # Request metrics
# REQUEST_COUNT = Counter(
#     'http_requests_total',
#     'Total number of HTTP requests',
#     ['method', 'endpoint', 'status']
# )

# REQUEST_LATENCY = Histogram(
#     'http_request_duration_seconds',
#     'HTTP request latency in seconds',
#     ['method', 'endpoint']
# )

# # Database metrics
# DB_OPERATION_COUNT = Counter(
#     'db_operations_total',
#     'Total number of database operations',
#     ['operation_type', 'table']
# )

# DB_OPERATION_LATENCY = Histogram(
#     'db_operation_duration_seconds',
#     'Database operation latency in seconds',
#     ['operation_type', 'table']
# )

# # Cache metrics
# CACHE_HITS = Counter(
#     'cache_hits_total',
#     'Total number of cache hits',
#     ['cache_name']
# )

# CACHE_MISSES = Counter(
#     'cache_misses_total',
#     'Total number of cache misses',
#     ['cache_name']
# )

# # System metrics
# ACTIVE_USERS = Gauge(
#     'active_users',
#     'Number of currently active users'
# )

# def track_request_metrics(func):
#     from functools import wraps
#     import time

#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         start_time = time.time()
#         try:
#             response = await func(*args, **kwargs)
#             # If response has status_code, use it; else, assume 200
#             status = getattr(response, "status_code", 200)
#         except Exception as e:
#             status = 500
#             raise e
#         finally:
#             request = kwargs.get('request')
#             if request:
#                 method = request.method
#                 endpoint = request.url.path
#             else:
#                 method = "UNKNOWN"
#                 endpoint = "UNKNOWN"
#             REQUEST_COUNT.labels(
#                 method=method,
#                 endpoint=endpoint,
#                 status=status
#             ).inc()
#             REQUEST_LATENCY.labels(
#                 method=method,
#                 endpoint=endpoint
#             ).observe(time.time() - start_time)
#         return response
#     return wrapper

# def track_db_operation(operation_type, table):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             start_time = time.time()
#             try:
#                 result = await func(*args, **kwargs)
#                 return result
#             finally:
#                 duration = time.time() - start_time
#                 DB_OPERATION_COUNT.labels(
#                     operation_type=operation_type,
#                     table=table
#                 ).inc()
#                 DB_OPERATION_LATENCY.labels(
#                     operation_type=operation_type,
#                     table=table
#                 ).observe(duration)
#         return wrapper
#     return decorator

# def track_cache_operation(cache_name):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             try:
#                 result = await func(*args, **kwargs)
#                 if result is not None:
#                     CACHE_HITS.labels(cache_name=cache_name).inc()
#                 else:
#                     CACHE_MISSES.labels(cache_name=cache_name).inc()
#                 return result
#             except Exception as e:
#                 CACHE_MISSES.labels(cache_name=cache_name).inc()
#                 raise e
#         return wrapper
#     return decorator 