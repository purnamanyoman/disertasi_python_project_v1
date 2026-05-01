import argparse
from preprocessing import preprocess_data, save_processed_data
from workload_generator import build_queries, generate_uniform_workload, generate_zipf_workload
from experiment_runner import run_experiments
from adaptive_model import AdaptiveModel, choose_best_config

def main():
    parser = argparse.ArgumentParser(description="Pipeline prototipe disertasi Bloom Filter dan Cuckoo Filter")
    parser.add_argument("--input", required=True, help="Path dataset CSV")
    parser.add_argument("--key", required=True, help="Nama kolom key pencarian")
    parser.add_argument("--workload", default="uniform", choices=["uniform", "zipf"], help="Jenis workload")
    args = parser.parse_args()

    df = preprocess_data(args.input, args.key)
    save_processed_data(df, "data/processed/processed_dataset.csv")

    keys = df[args.key].tolist()
    positive_queries, negative_queries = build_queries(keys, n_positive=1000, n_negative=1000)

    if args.workload == "zipf":
        workload = generate_zipf_workload(keys, n_queries=5000)
    else:
        workload = generate_uniform_workload(keys, n_queries=5000)

    df_results = run_experiments(
        keys=keys,
        negative_queries=negative_queries,
        workload=workload,
        output_csv="results/experiments.csv"
    )

    model = AdaptiveModel()
    model.fit(df_results, ["fpr", "latency", "throughput", "memory"])

    candidate_configs = [
        {"fp_rate_target": 0.01, "bucket_size": 2, "fingerprint_size": 8},
        {"fp_rate_target": 0.05, "bucket_size": 4, "fingerprint_size": 16},
        {"fp_rate_target": 0.10, "bucket_size": 4, "fingerprint_size": 8},
    ]
    best_config, best_metrics = choose_best_config(model, candidate_configs)

    print("=== Hasil eksperimen ===")
    print(df_results)
    print("\n=== Konfigurasi terbaik ===")
    print(best_config)
    print(best_metrics)

if __name__ == "__main__":
    main()
