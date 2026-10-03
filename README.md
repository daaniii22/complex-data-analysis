# Multimodal Climate Time Series

Dataset multimodal semanal que combina señales climáticas y económicas con atención mediática y texto histórico de Wikipedia. El recurso está preparado para análisis exploratorio, extracción de características, embeddings y modelos de series temporales. La documentación FAIR completa se encuentra en [`metadata.md`](metadata.md).

## Contenido del repositorio

- [`dataset_creation.ipynb`](dataset_creation.ipynb): pipeline de descarga, alineación temporal, control de calidad y exportación.
- `data/raw/dataset_clima_multimodal_fair.parquet`: artefacto Parquet listo para subir manualmente a Hugging Face Datasets.
- [`metadata.md`](metadata.md): ficha del dataset, procedencia, esquema, licencias, limitaciones y criterios FAIR.

Los archivos `intent.md` y `push_to_hub.py` no forman parte del flujo de publicación manual descrito aquí.

## Esquema

Cada fila representa una fecha semanal (domingo) y contiene el texto de la entradilla de `Climate change` en Wikipedia junto con estas señales:

`id`, `timestamp`, `text`, `co2_ppm`, `brent_price`, `temp_anomaly_c`, `ch4_ppb`, `n2o_ppb`, `oni_anomaly`, `media_volume_norm`, `rev_id`, `rev_timestamp`, `rev_size`, `source_text`, `source_metrics` y `domain`.

Las columnas de texto y fecha están en inglés para facilitar la interoperabilidad con herramientas de datos. `timestamp` es una fecha sin zona horaria normalizada a la cuadrícula semanal; las medidas numéricas conservan sus unidades originales, descritas en [`metadata.md`](metadata.md).

## Uso local

```bash
python3 -m pip install -r requirements.txt
```

Abre `dataset_creation.ipynb` y ejecuta las celdas en orden. El pipeline usa APIs públicas y puede tardar, especialmente al recuperar las revisiones de Wikipedia. Al finalizar genera:

```text
data/raw/dataset_clima_multimodal.parquet
data/raw/dataset_clima_multimodal_fair.parquet
```

Para inspeccionar el Parquet:

```python
import pandas as pd

df = pd.read_parquet("data/raw/dataset_clima_multimodal_fair.parquet")
print(df.shape)
print(df.head())
```

## Publicación manual en Hugging Face

1. Crea un repositorio de tipo **Dataset**.
2. Sube `data/raw/dataset_clima_multimodal_fair.parquet` como archivo Parquet.
3. Usa esta ficha y [`metadata.md`](metadata.md) para completar la tarjeta del dataset y sus etiquetas.
4. Comprueba en la vista previa que `timestamp` se interpreta como fecha y que el texto se muestra correctamente.

Al subir un Parquet sin particiones explícitas, Hugging Face Datasets lo suele presentar como la partición `train`. El archivo de origen no contiene una partición train/test: cualquier división para experimentación debe hacerse respetando el orden temporal y documentarse en el estudio que la utilice.

## Reproducibilidad y limitaciones

Las APIs son fuentes vivas: una nueva ejecución puede devolver revisiones, precios o valores corregidos distintos. El notebook conserva identificadores deterministas por registro, pero el resultado solo es idéntico si las fuentes remotas no han cambiado. GDELT puede no responder durante una ejecución; el pipeline registra esta situación y usa una señal proxy derivada de los cambios de longitud del texto, que debe identificarse como tal antes de cualquier análisis científico.

La continuidad semanal se audita, pero no se imputan silenciosamente valores faltantes. Revisa los nulos y el linaje de cada columna antes de ajustar modelos causales. La asociación temporal no demuestra causalidad.

## Licencia y atribución

El código de este repositorio se distribuye bajo la licencia MIT indicada en [`LICENSE`](LICENSE). Los datos agregados deben respetar las condiciones de sus fuentes: el texto de Wikipedia se ofrece bajo CC BY-SA 4.0, las series de NOAA y NASA son datos públicos del Gobierno de Estados Unidos, Yahoo Finance impone sus propias condiciones de uso y GDELT debe citarse según sus términos. Consulta [`metadata.md`](metadata.md) antes de redistribuir o reutilizar el dataset.
