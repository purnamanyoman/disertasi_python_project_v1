import random
import numpy as np

def build_queries(keys, n_positive=1000, n_negative=1000):
    if not keys:
        return [], [f"neg_key_{i}" for i in range(n_negative)]
    n_positive = min(n_positive, len(keys))
    positive_queries = random.sample(keys, n_positive)
    negative_queries = [f"neg_key_{i}" for i in range(n_negative)]
    return positive_queries, negative_queries

def generate_uniform_workload(keys, n_queries=1000):
    if not keys:
        return []
    return random.choices(keys, k=n_queries)

def generate_zipf_workload(keys, n_queries=1000, s=1.2):
    if not keys:
        return []
    ranks = np.arange(1, len(keys) + 1)
    probs = 1 / np.power(ranks, s)
    probs = probs / probs.sum()
    return list(np.random.choice(keys, size=n_queries, p=probs))
