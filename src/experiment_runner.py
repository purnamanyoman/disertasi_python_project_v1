from pathlib import Path
import pandas as pd
from bloom_filter import BloomFilter
from cuckoo_filter import CuckooFilter
from evaluator import calculate_fpr, measure_latency, measure_throughput, get_memory_usage

def run_experiments(keys, negative_queries, workload, output_csv):
    results = []
    bf_fp_rates = [0.1, 0.05, 0.01]
    cf_bucket_sizes = [2, 4]
    cf_fps = [8, 16]

    for fp_rate in bf_fp_rates:
        bf = BloomFilter(n_items=len(keys), fp_rate=fp_rate)
        for key in keys:
            bf.add(key)
        results.append({
            "structure": "BloomFilter",
            "fp_rate_target": fp_rate,
            "bucket_size": 0,
            "fingerprint_size": 0,
            "fpr": calculate_fpr(bf, negative_queries),
            "latency": measure_latency(bf, workload),
            "throughput": measure_throughput(bf, workload),
            "memory": get_memory_usage(bf),
        })

    for bucket_size in cf_bucket_sizes:
        for fp_size in cf_fps:
            cf = CuckooFilter(capacity=max(10, len(keys) * 2), bucket_size=bucket_size, fingerprint_size=fp_size)
            for key in keys:
                cf.insert(key)
            results.append({
                "structure": "CuckooFilter",
                "fp_rate_target": 0,
                "bucket_size": bucket_size,
                "fingerprint_size": fp_size,
                "fpr": calculate_fpr(cf, negative_queries),
                "latency": measure_latency(cf, workload),
                "throughput": measure_throughput(cf, workload),
                "memory": get_memory_usage(cf),
            })

    df_results = pd.DataFrame(results)
    output_file = Path(output_csv)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_results.to_csv(output_file, index=False)
    return df_results
