---
annotations_creators:
- no-annotation
language:
- en
language_creators:
- crowdsourced
- machine-generated
license: mit
multilinguality:
- monolingual
pretty_name: Multimodal Climate Time Series (2008-2026)
size_categories:
- n<1K
source_datasets:
- original
tags:
- climate-change
- time-series
- multimodal
- nlp
- causal-inference
task_categories:
- feature-extraction
- time-series-forecasting
---

# Dataset Card: Multimodal Climate Time Series (2008–2026)

## 1. Dataset Summary
* **Propósito y Contexto:** Este dataset multimodal ha sido desarrollado en el marco de la asignatura *Descubrimiento de Conocimiento en Datos Complejos* (ETSISI - Universidad Politécnica de Madrid). Su objetivo es estudiar la dinámica temporal y las relaciones causales (en sentido de Granger) entre tres dimensiones heterogéneas:
  1. *Variables Físico-Económicas:* Concentraciones troposféricas de $CO_2$, $CH_4$, $N_2O$, anomalías térmicas globales (NASA GISTEMP), índice oceánico El Niño (ONI) y cotizaciones de futuros del crudo Brent.
  2. *Atención Mediática Internacional:* Volumen normalizado de cobertura global en prensa digital sobre cambio climático extraído mediante GDELT 2.0 Doc API.
  3. *Narrativa Pública Colaborativa:* Evolución textual y velocidad de cambio semántico de la entradilla del artículo *Climate change* de Wikipedia en inglés.
* **Granularidad:** Muestreo semanal estricto (`W-SUN`, domingos) que abarca desde enero de 2008 hasta septiembre de 2026 (977 observaciones continuas).
* **Justificación Metodológica:** Para la estimación de modelos autorregresivos (VAR) y contrastes de causalidad temporal, se prioriza una serie longitudinal extensa y homogénea de 18+ años equiespaciados frente a un gran volumen no estructurado, evitando la introducción de datos imputados artificialmente.

## 2. How to use
El conjunto de datos se distribuye con una partición temporal estricta (80% entrenamiento / 20% prueba) para prevenir la fuga de información hacia el pasado (*look-ahead bias*).

```python
from datasets import load_dataset

# Carga del dataset desde Hugging Face Hub
dataset = load_dataset("daaniii22/complex-data-analysis")

# Inspección de las particiones temporales
print(dataset)
sample = dataset["train"][0]
print("Fecha:", sample["timestamp"])
print("CO2 (ppm):", sample["co2_ppm"])
print("Extracto de Wikipedia:", sample["text"][:120])
``` 

## 3. Dataset Details
### 3.1. Data Structure

Cada fila corresponde a una observación semanal consolidada con los siguientes campos y metadatos:

* `id` (`string`): Identificador único universal inmutable (UUIDv4) por registro.
* `timestamp` (`timestamp[ns]`): Fecha de referencia semanal (domingo).
* `text` (`string`): Texto íntegro de la entradilla (*lead section*) de Wikipedia vigente en dicha fecha.
* `co2_ppm` (`float64`): Promedio semanal de concentración de $CO_2$ en Mauna Loa (NOAA GML).
* `brent_price` (`float64`): Precio de cierre ajustado semanal de los futuros de petróleo Brent en USD (Yahoo Finance).
* `temp_anomaly_c` (`float64`): Anomalía de temperatura media global superficial (NASA GISTEMP v4).
* `ch4_ppb` (`float64`): Concentración mensual global de metano en partes por billón (NOAA GML).
* `n2o_ppb` (`float64`): Concentración mensual global de óxido nitroso en partes por billón (NOAA GML).
* `oni_anomaly` (`float64`): Índice de anomalía oceánica El Niño/La Niña (NOAA CPC).
* `media_volume_norm` (`float64`): Volumen relativo normalizado de cobertura en medios (GDELT 2.0).
* `rev_id` (`int64`): Identificador único numérico de la revisión en MediaWiki.
* `rev_timestamp` (`string`): Marca temporal ISO 8601 de publicación de la revisión.
* `source_text` (`string`): Procedencia de la señal textual (`Wikipedia (en)`).
* `source_metrics` (`string`): Fuentes de las variables numéricas y económicas.
* `domain` (`string`): Dominio de aplicación (`Climate Change Multimodal Time Series`).

### 3.2. Data Preview
Muestra sintética representativa de registros en el corte semanal:

| timestamp | brent_price | co2_ppm | temp_anomaly_c | media_volume_norm | rev_id | text (fragmento inicial) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2008-01-06` | 94.39 | 385.02 | 0.30 | 0.0000 | 181256649 | `{{protected}}{{featured article}} Global warming is the increase in the average temperature...` |
| `2016-03-27` | 40.47 | 404.83 | 1.34 | 0.1284 | 711660458 | `Climate change includes both global warming driven by human emissions of greenhouse gases...` |
| `2026-09-20` | 78.50 | 426.15 | 1.18 | 0.3412 | 1376019004 | `Contemporary climate change includes both global warming caused by humans and its impacts...` |

### 3.3. Data Collection
* **Metodología e Instrumentación:** Pipeline de extracción automatizado mediante llamadas a APIs públicas y repositorios abiertos oficiales:
  * *Wikipedia:* Ingesta de revisiones históricas retrospectivas (`action=query`, `prop=revisions`, `rvdir=older`, `rvsection=0`) limitadas a la sección de introducción para preservar consistencia estilística y sintáctica.
  * *NOAA GML & CPC:* Series directas de $CO_2$ semanal en Mauna Loa, medias globales mensuales de $CH_4$ y $N_2O$, e índice trimestral centrado ONI.
  * *NASA GISS:* Tablas reticulares consolidadas de anomalías térmicas GISTEMP v4.
  * *Mercados Energéticos:* Contratos continuos de crudo Brent (`BZ=F`) mediante la API de Yahoo Finance.
  * *Prensa Global:* API de GDELT 2.0 Doc (`timelinevol`) en formato tabular normalizado.
* **Marco Temporal:** Registro continuo desde el 01/01/2008 hasta el 22/09/2026 (977 semanas).
* **Control de Muestreo:** Fijación semanal regular a domingos (`W-SUN`) para independizar el índice de festivos y cierres de mercados financieros.

### 3.4. Data Processing
* **Tratamiento de Look-Ahead Bias:** Las métricas publicadas de forma mensual consolidada (anomalías térmicas de NASA y concentraciones de gases de NOAA) se indexan con un desfase al primer día del mes siguiente ($M \to M+1$) antes de realizar la unión temporal hacia atrás (`pd.merge_asof(direction='backward')`), garantizando que los datos no estén accesibles al modelo antes de su fecha real de publicación.
* **Integridad Numérica:** Cobertura exhaustiva con 0 valores nulos (`NaN`) en la totalidad de las 977 observaciones consolidadas.
* **Procesamiento Textual:** Conservación íntegra de la sintaxis wikitext para permitir la posterior extracción de embeddings densos y métricas de distancia del coseno sobre estados textuales idénticos.

### 3.5. Data Maintenance
* **Alojamiento y Versionado:** Repositorio en GitHub (`daaniii22/complex-data-analysis`) y Hugging Face Datasets (`daaniii22/complex-data-analysis`).
* **Autores:** 
  * Daniel Moraleda Sánchez
  * Miguel Ángel Morera Hernández
  * Víctor Pastor López
  * David Santiago Ruiz
  * Juan Pablo Asenjo Seoanes
* **Institución:** Escuela Técnica Superior de Ingeniería de Sistemas Informáticos (ETSISI), Universidad Politécnica de Madrid (UPM).
* **Política de Actualización:** Dataset congelado para la experimentación académica de la asignatura; ampliable y reproducible mediante el código provisto en el repositorio.

## 4. License
El código fuente y la consolidación del conjunto de datos se distribuyen bajo la licencia **MIT License**:

```text
MIT License

Copyright (c) 2026 Daniel Moraleda Sánchez, Miguel Ángel Morera Hernández,
Víctor Pastor López, David Santiago Ruiz, Juan Pablo Asenjo Seoanes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

> **Atribución de fuentes originales:**
> * Los contenidos textuales extraídos de Wikipedia están sujetos a la licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.
> * Los registros climáticos de NOAA y NASA pertenecen al dominio público del Gobierno Federal de los Estados Unidos.
> * Las series temporales de cobertura mediática se consultan bajo los términos de acceso abierto con fines de investigación de GDELT Project.

## 5. Citation
Formato de citación recomendado para este recurso:

```bibtex
@dataset{clima_multimodal_upm_2026,
  author       = {Moraleda Sánchez, Daniel and 
                  Morera Hernández, Miguel Ángel and 
                  Pastor López, Víctor and 
                  Santiago Ruiz, David and 
                  Asenjo Seoanes, Juan Pablo},
  title        = {Multimodal Climate Time Series: Physical Signals, Media Coverage and Public Narrative (2008--2026)},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/daaniii22/complex-data-analysis}}
}
```

## 6. Acknowledgements

Agradecimientos al equipo docente de la asignatura Descubrimiento de Conocimiento en Datos Complejos de la Escuela Técnica Superior de Ingeniería de Sistemas Informáticos (UPM), así como a las iniciativas de ciencia abierta y datos públicos de Wikimedia Foundation, NOAA GML, NASA GISS y GDELT Project.