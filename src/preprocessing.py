from pathlib import Path
import pandas as pd

def preprocess_data(file_path: str, key_column: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    if key_column not in df.columns:
        raise ValueError(f"Kolom '{key_column}' tidak ditemukan pada dataset.")
    df = df.dropna(subset=[key_column])
    df = df.drop_duplicates(subset=[key_column])
    df[key_column] = df[key_column].astype(str).str.strip().str.lower()
    return df

def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
