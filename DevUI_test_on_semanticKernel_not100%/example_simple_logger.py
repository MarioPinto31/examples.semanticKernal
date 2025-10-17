from prometheus_client import Counter, Histogram, start_http_server
import time

# Create metrics
sk_calls = Counter("sk_function_calls_total", "Total SK function calls")
sk_latency = Histogram("sk_function_latency_seconds", "Latency of SK function calls")

# Start Prometheus HTTP endpoint
start_http_server(8000)  # exposes metrics on http://localhost:8000/metrics

def tracked_function(func):
    def wrapper(*args, **kwargs):
        sk_calls.inc()
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            sk_latency.observe(time.time() - start_time)
    return wrapper

# Example SK call with tracking
@tracked_function
def run_sk_task():
    # Your semantic kernel function call here
    time.sleep(0.5)
