---
annotations_creators:
- no-annotation
language:
- en
language_creators:
- machine-generated
license: mit
multilinguality:
- monolingual
pretty_name: Multimodal Climate Time Series
size_categories:
- n<1K
source_datasets:
- original
tags:
- climate-change
- time-series
- multimodal
- nlp
- wikipedia
- gdelt
task_categories:
- feature-extraction
- text-classification
---

# Multimodal Climate Time Series (2008–2026)

## 1. Dataset Summary

Este dataset reúne una observación semanal continua desde enero de 2008 hasta septiembre de 2026 (977 registros) para estudiar la relación temporal entre señales climáticas, macroeconómicas, mediáticas y narrativas. Cada registro combina mediciones numéricas oficiales con la entradilla histórica del artículo *Climate change* de Wikipedia en inglés correspondiente a la fecha de referencia.

El recurso está diseñado para análisis exploratorio, extracción de embeddings densos, cuantificación de velocidad semántica y modelado temporal (VAR / Granger). Las relaciones observadas deben evaluarse con rigor metodológico y no interpretarse de forma determinista sin la debida identificación econométrica.

## 2. How to use

El artefacto se encuentra estructurado en formato Parquet y puede cargarse directamente mediante la librería `datasets` de Hugging Face o con `pandas`:

```python
from datasets import load_dataset

# Carga directa del dataset desde Hugging Face Hub
dataset = load_dataset("miguel-mxrxra04/multimodal-climate-change-2008-2026")

# Inspección de variables
sample = dataset["train"][0]
print("Semana:", sample["timestamp"])
print("CO2 (ppm):", sample["co2_ppm"])
print("Texto de Wikipedia:", sample["text"][:120])
```
## 3. Dataset Details
###  3.1 Data Structure

| Campo | Tipo esperado | Descripción y unidad |
|---|---|---|
| `id` | string | UUIDv5 determinista basado en artículo, fecha y revisión. |
| `timestamp` | datetime | Domingo de la semana de referencia. |
| `text` | string | Entradilla histórica de Wikipedia, en inglés, en wikitext. |
| `co2_ppm` | float | CO2 semanal de Mauna Loa, partes por millón. |
| `brent_price` | float | Cierre semanal del futuro Brent, USD. |
| `temp_anomaly_c` | float | Anomalía mensual GISTEMP, grados Celsius. |
| `ch4_ppb` | float | Concentración global mensual de metano, partes por billón. |
| `n2o_ppb` | float | Concentración global mensual de óxido nitroso, partes por billón. |
| `oni_anomaly` | float | Anomalía ONI de NOAA CPC, grados Celsius. |
| `media_volume_norm` | float | Volumen relativo normalizado de cobertura de GDELT; puede ser proxy. |
| `rev_id` | integer | Identificador de revisión de MediaWiki. |
| `rev_timestamp` | string | Marca temporal ISO 8601 de la revisión. |
| `rev_size` | integer | Tamaño de la revisión de MediaWiki en bytes. |
| `source_text` | string | Procedencia de la señal textual. |
| `source_metrics` | string | Procedencia de las señales numéricas. |
| `domain` | string | Dominio común del recurso. |

El artefacto publicado es un único Parquet. No contiene particiones train/test; Hugging Face puede mostrarlo como `train` al cargarlo, pero esa etiqueta no representa una división metodológica. Las divisiones para experimentación deben respetar el orden temporal y crearse fuera del artefacto original.

### 3.2 Data Collection

El notebook obtiene datos de APIs o repositorios públicos de Wikipedia/MediaWiki, NOAA GML, NOAA CPC, NASA GISTEMP, Yahoo Finance y GDELT. Las series se alinean mediante `merge_asof(direction="backward")` sobre una cuadrícula semanal `W-SUN`. Los datos mensuales se indexan al primer día del mes siguiente para evitar usar una medición mensual antes de su fecha de disponibilidad modelada.

La revisión de Wikipedia se selecciona con la última revisión disponible hasta cada fecha objetivo. El contenido conserva wikitext para no perder información durante la captura; quien necesite texto limpio debe aplicar un parser y documentar esa transformación.

Si GDELT no responde, el notebook genera una señal proxy basada en la variación de longitud del texto. Esta columna debe inspeccionarse y marcarse como proxy en cualquier análisis que la utilice; no es una medición equivalente de cobertura mediática.

### 3.3. Data Processing
El pipeline verifica de forma estricta las columnas esperadas, la unicidad de `id`, el orden temporal y la regularidad semanal de 7 días, notificando valores anómalos sin realizar imputaciones forzadas. 

Las fuentes remotas pueden revisar su histórico con el tiempo, por lo que una nueva ejecución del pipeline podría incorporar ajustes retroactivos de las agencias emisoras.

### 3.4. Biases and limitations
El dataset contiene sesgos propios de la cobertura editorial de Wikipedia en inglés, la selección periodística de la prensa digital y la dinámica de los mercados financieros. La disponibilidad del texto no equivale a una muestra probabilística de la opinión pública global. 

Asimismo, el muestreo semanal puede suavizar eventos de impacto subsemanal. Las relaciones identificadas corresponden a correlaciones y precedencias temporales; no deben inferirse afirmaciones causales definitivas sin un diseño de identificación econométrico completo.

### 3.5. Data Maintenance
* **Alojamiento:** Repositorio en GitHub (`daaniii22/complex-data-analysis`) y Hugging Face Datasets (`miguel-mxrxra04/multimodal-climate-change-2008-2026`).
* **Autores:** Daniel Moraleda Sánchez, Miguel Ángel Morera Hernández, Víctor Pastor López, David Santiago Ruiz y Juan Pablo Asenjo Seoanes (ETSISI - UPM).
* **Ciclo de vida:** El dataset se mantiene congelado para la experimentación académica de la asignatura y es completamente reproducible mediante la ejecución del notebook `dataset_creation.ipynb`.

## 4. License

El código de este repositorio está bajo MIT. La redistribución del dataset debe respetar las licencias y términos de las fuentes:

- Wikipedia: CC BY-SA 4.0, con atribución y obligación de compartir bajo la misma licencia las adaptaciones del contenido cubierto por ella.
- NOAA y NASA: datos públicos del Gobierno de Estados Unidos, sujetos a sus avisos y condiciones de cada producto.
- GDELT Project: consultar y citar los términos del proyecto antes de reutilizar la señal mediática.
- Yahoo Finance: consultar sus condiciones de uso y redistribución para los precios de mercado.

La etiqueta `cc-by-sa-4.0` del front matter describe principalmente el contenido textual reutilizado; no sustituye las condiciones específicas de las demás fuentes.

## 5. Citation

El dataset se congela para el trabajo académico y se puede regenerar ejecutando `dataset_creation.ipynb`. La fecha de descarga y las versiones de las fuentes deben registrarse cuando se publique una nueva versión en Hugging Face.

```bibtex
@dataset{multimodal_climate_time_series_2026,
  author    = {Moraleda Sánchez, Daniel and 
               Morera Hernández, Miguel Ángel and 
               Pastor López, Víctor and 
               Santiago Ruiz, David and 
               Asenjo Seoanes, Juan Pablo},
  title     = {Multimodal Climate Time Series: Physical Signals, Media Coverage and Public Narrative (2008--2026)},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/miguel-mxrxra04/multimodal-climate-change-2008-2026}
}
```

## 6. Acknowledgements

Agradecimientos al equipo docente de la asignatura Descubrimiento de Conocimiento en Datos Complejos de la Escuela Técnica Superior de Ingeniería de Sistemas Informáticos (ETSISI - UPM), y a las iniciativas de datos abiertos de Wikimedia Foundation, NOAA Global Monitoring Laboratory, NOAA Climate Prediction Center, NASA Goddard Institute for Space Studies, GDELT Project y Yahoo Finance por posibilitar el acceso público a sus registros históricos.
