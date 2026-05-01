import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class AdaptiveModel:
    def __init__(self):
        self.model_fpr = RandomForestRegressor(random_state=42)
        self.model_latency = RandomForestRegressor(random_state=42)
        self.model_throughput = RandomForestRegressor(random_state=42)
        self.model_memory = RandomForestRegressor(random_state=42)
        self.features = []

    def fit(self, df: pd.DataFrame, target_cols):
        self.features = [c for c in df.columns if c not in target_cols and c != "structure"]
        X = df[self.features].fillna(0)
        models = {
            "fpr": self.model_fpr,
            "latency": self.model_latency,
            "throughput": self.model_throughput,
            "memory": self.model_memory,
        }
        for target_name, model in models.items():
            if target_name in df.columns:
                y = df[target_name].fillna(0)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model.fit(X_train, y_train)

    def predict_metrics(self, config):
        row = pd.DataFrame([{f: config.get(f, 0) for f in self.features}])
        return {
            "fpr": float(self.model_fpr.predict(row)[0]),
            "latency": float(self.model_latency.predict(row)[0]),
            "throughput": float(self.model_throughput.predict(row)[0]),
            "memory": float(self.model_memory.predict(row)[0]),
        }

def objective_function(fpr, latency, throughput, memory, w1=0.3, w2=0.3, w3=0.2, w4=0.2):
    return (w1 * fpr) + (w2 * latency) + (w3 * memory) - (w4 * throughput)

def choose_best_config(model, candidate_configs):
    best_config = None
    best_metrics = None
    best_score = float("inf")
    for config in candidate_configs:
        metrics = model.predict_metrics(config)
        score = objective_function(metrics["fpr"], metrics["latency"], metrics["throughput"], metrics["memory"])
        if score < best_score:
            best_score = score
            best_config = config
            best_metrics = metrics
    return best_config, best_metrics
