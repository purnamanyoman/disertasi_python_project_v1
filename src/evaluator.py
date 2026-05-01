import sys
import time
try:
    from pympler import asizeof
    HAS_PYMPLER = True
except Exception:
    HAS_PYMPLER = False

def calculate_fpr(filter_obj, negative_queries):
    if not negative_queries:
        return 0.0
    false_positive = 0
    for q in negative_queries:
        if filter_obj.contains(q):
            false_positive += 1
    return false_positive / len(negative_queries)

def measure_latency(filter_obj, queries):
    if not queries:
        return 0.0
    start = time.perf_counter()
    for q in queries:
        filter_obj.contains(q)
    end = time.perf_counter()
    return (end - start) / len(queries)

def measure_throughput(filter_obj, queries):
    if not queries:
        return 0.0
    start = time.perf_counter()
    for q in queries:
        filter_obj.contains(q)
    end = time.perf_counter()
    total = end - start
    return 0.0 if total == 0 else len(queries) / total

def get_memory_usage(obj):
    if HAS_PYMPLER:
        return int(asizeof.asizeof(obj))
    return int(sys.getsizeof(obj))
