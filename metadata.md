---
annotations_creators:
- no-annotation
language:
- en
language_creators:
- machine-generated
license:
- cc-by-sa-4.0
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

# Multimodal Climate Time Series

## Resumen

Este dataset reúne una observación semanal desde 2008 para estudiar la relación temporal entre señales climáticas, económicas, mediáticas y textuales. Cada registro combina medidas numéricas con la entradilla histórica del artículo `Climate change` de Wikipedia en inglés correspondiente a la fecha de referencia.

El recurso está diseñado para análisis exploratorio, extracción de embeddings, comparación de cambios textuales y modelado temporal. Las relaciones observadas no deben interpretarse como evidencia de causalidad: el dataset no incluye una identificación causal experimental.

## Acceso y localización (FAIR)

- **Findable:** el Parquet tiene nombres de columnas estables, un `id` global determinista por registro, un esquema documentado y una tarjeta preparada para el repositorio de Hugging Face `daaniii22/complex-data-analysis`.
- **Accessible:** el artefacto se distribuye como Parquet, un formato abierto y legible con pandas, PyArrow y Hugging Face Datasets. La publicación manual se realiza subiendo `data/raw/dataset_clima_multimodal_fair.parquet`.
- **Interoperable:** fechas ISO se exponen en `timestamp`, el texto está en `text`, las unidades aparecen en el esquema y el formato columnar conserva los tipos de datos.
- **Reusable:** el notebook documenta la extracción, la alineación temporal, el linaje, las validaciones y las limitaciones. Deben respetarse las licencias de cada fuente antes de redistribuir el contenido.

## Esquema

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

## Recogida y procesamiento

El notebook obtiene datos de APIs o repositorios públicos de Wikipedia/MediaWiki, NOAA GML, NOAA CPC, NASA GISTEMP, Yahoo Finance y GDELT. Las series se alinean mediante `merge_asof(direction="backward")` sobre una cuadrícula semanal `W-SUN`. Los datos mensuales se indexan al primer día del mes siguiente para evitar usar una medición mensual antes de su fecha de disponibilidad modelada.

La revisión de Wikipedia se selecciona con la última revisión disponible hasta cada fecha objetivo. El contenido conserva wikitext para no perder información durante la captura; quien necesite texto limpio debe aplicar un parser y documentar esa transformación.

Si GDELT no responde, el notebook genera una señal proxy basada en la variación de longitud del texto. Esta columna debe inspeccionarse y marcarse como proxy en cualquier análisis que la utilice; no es una medición equivalente de cobertura mediática.

## Calidad, sesgos y limitaciones

El pipeline comprueba columnas esperadas, unicidad de `id`, orden temporal y saltos semanales distintos de siete días, e informa de los valores nulos sin imputarlos automáticamente. Las fuentes remotas pueden revisar su histórico, por lo que una nueva ejecución no garantiza byte a byte el mismo Parquet.

El dataset contiene sesgos de cobertura de Wikipedia, prensa digital y fuentes financieras. La disponibilidad del texto no implica representatividad de la opinión pública. El muestreo semanal puede ocultar eventos de corta duración y las distintas frecuencias originales no eliminan la incertidumbre de fecha de publicación. No se deben inferir efectos causales solo a partir de correlaciones o pruebas de Granger.

## Licencia y atribución

El código de este repositorio está bajo MIT. La redistribución del dataset debe respetar las licencias y términos de las fuentes:

- Wikipedia: CC BY-SA 4.0, con atribución y obligación de compartir bajo la misma licencia las adaptaciones del contenido cubierto por ella.
- NOAA y NASA: datos públicos del Gobierno de Estados Unidos, sujetos a sus avisos y condiciones de cada producto.
- GDELT Project: consultar y citar los términos del proyecto antes de reutilizar la señal mediática.
- Yahoo Finance: consultar sus condiciones de uso y redistribución para los precios de mercado.

La etiqueta `cc-by-sa-4.0` del front matter describe principalmente el contenido textual reutilizado; no sustituye las condiciones específicas de las demás fuentes.

## Mantenimiento y citación

El dataset se congela para el trabajo académico y se puede regenerar ejecutando `dataset_creation.ipynb`. La fecha de descarga y las versiones de las fuentes deben registrarse cuando se publique una nueva versión en Hugging Face.

```bibtex
@dataset{multimodal_climate_time_series,
  author    = {Moraleda Sánchez, Daniel and Morera Hernández, Miguel Ángel and
               Pastor López, Víctor and Santiago Ruiz, David and
               Asenjo Seoanes, Juan Pablo},
  title     = {Multimodal Climate Time Series},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/daaniii22/complex-data-analysis}
}
```

## Agradecimientos

A las fuentes abiertas y a sus equipos de mantenimiento: Wikimedia Foundation, NOAA GML, NOAA CPC, NASA GISS, GDELT Project y Yahoo Finance, así como al equipo docente de la asignatura Descubrimiento de Conocimiento en Datos Complejos de la ETSISI, Universidad Politécnica de Madrid.
