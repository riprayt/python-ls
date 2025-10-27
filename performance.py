from functools import wraps
import time

def measure_time(func):
    """Decorator to measure the execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        print(f"Execution time of {func.__name__}: {t1 - t0:.4f} seconds")
        return result
    return wrapper

@measure_time
def run_performance_tests():
    total = 0
    for i in range(1, 100000000):
        total += i ** 2
    print(f"Total sum of squares: {total}")

if __name__ == "__main__":
    run_performance_tests()
