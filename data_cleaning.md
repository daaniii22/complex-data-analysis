# Data Cleaning — Entrega 2

## 1. Dataset original

- Fuente: Hugging Face, `miguel-mxrxra04/multimodal-climate-change-2008-2026`
- Observaciones: 978 (frecuencia semanal); texto de la entradilla de Wikipedia en inglés

## 2. Revisión de las columnas numéricas

- Fechas ordenadas y sin duplicados; nulos en columnas numéricas: 0.
- Las series mensuales (temperatura, CH4, N2O, ONI) se repiten en las semanas de cada mes.
  Porcentaje de semanas con el mismo valor que la semana anterior:
  - `co2_ppm`: 1%
  - `brent_price`: 1%
  - `temp_anomaly_c`: 78%
  - `ch4_ppb`: 77%
  - `n2o_ppb`: 77%
  - `oni_anomaly`: 77%
  - `media_volume_norm`: 24%
  - `rev_size`: 10%
- `media_volume_norm` (cobertura mediática de GDELT) es un proxy, con valores casi siempre cercanos a 0.

## 3. Transformaciones aplicadas al texto

1. Eliminación de comentarios HTML.
2. Plantillas con contenido (`convert`, `CO2`, `CH4`, `N2O`, `nowrap`, `chem`...) sustituidas por su texto visible, para no dejar huecos al borrar plantillas.
3. Eliminación de imágenes, referencias y resto de plantillas con `mwparserfromhell`.
4. Normalización: Unicode NFKC, comillas y guiones unificados, restos de citas en bloque y espacios (columna `text_clean`).
   No se pasa a minúsculas ni se eliminan stopwords: se hace dentro de cada indicador.
5. Columnas añadidas: `text_id`, `texto_nuevo`, `anio`, `mes`.
6. Eliminación de duplicados: 602 observaciones repiten un texto anterior.
   Se guardan dos versiones: la serie semanal completa y los textos únicos.

## 4. Resultados

- Observaciones: 978 (la ficha de Hugging Face indica 977 registros, el dataset descargado tiene 978)
- Textos únicos: 376
- Semanas con texto distinto al de la semana anterior: 380. Es mayor que el número de textos únicos
  porque en 4 semanas el artículo vuelve a un texto ya visto (p. ej. reversiones de ediciones).
- Textos vacíos: 0

## 5. Limitaciones

- Un único artículo de Wikipedia y solo su entradilla, con estilo enciclopédico (sentimiento poco expresivo).
- Elevada repetición: el texto cambia poco de una semana a otra.
- Texto original en inglés (se traduce al español para el sentimiento).

## 6. Archivos generados

- `data/processed/dataset_clean.parquet`
- `data/processed/textos_unicos.parquet`
