import os
import pandas as pd
from datasets import Dataset, DatasetDict

# 1. Configuración del repositorio en Hugging Face
REPO_ID = "daaniii22/complex-data-analysis"

# Ruta del artefacto FAIR
FILE_PATH = "data/raw/dataset_clima_multimodal_fair.parquet"
if not os.path.exists(FILE_PATH):
    FILE_PATH = "dataset_clima_multimodal_fair.parquet"

print(f"Cargando dataset desde: {FILE_PATH}...")
df = pd.read_parquet(FILE_PATH)

# Asegurar ordenación cronológica estricta por timestamp
df = df.sort_values("timestamp").reset_index(drop=True)

# 2. Partición temporal (80% train / 20% test) sin shuffle para series temporales
split_idx = int(len(df) * 0.8)
df_train = df.iloc[:split_idx].copy()
df_test = df.iloc[split_idx:].copy()

print(f"Total registros: {len(df)}")
print(
    f" - Train (80%): {len(df_train)} semanas ({df_train['timestamp'].min().date()} a {df_train['timestamp'].max().date()})"
)
print(
    f" - Test  (20%): {len(df_test)} semanas ({df_test['timestamp'].min().date()} a {df_test['timestamp'].max().date()})"
)

# 3. Conversión a formato Hugging Face DatasetDict
hf_dataset = DatasetDict(
    {
        "train": Dataset.from_pandas(df_train, preserve_index=False),
        "test": Dataset.from_pandas(df_test, preserve_index=False),
    }
)

# 4. Publicación en el Hub
print(f"\nSubiendo particiones a Hugging Face: {REPO_ID}...")
hf_dataset.push_to_hub(REPO_ID, private=False)

print("✅ Dataset publicado exitosamente en Hugging Face Hub.")
