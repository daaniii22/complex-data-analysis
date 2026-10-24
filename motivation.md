# Motivación del proyecto — Entrega 2

## 1. Objetivo general

Estudiar cómo evoluciona, entre 2008 y 2026, el texto de la entradilla del artículo de Wikipedia en inglés *Climate change* y cómo se relaciona con señales externas: la publicación de informes del IPCC y varias series climáticas, energéticas y mediáticas.

Se parte del dataset FAIR multimodal publicado en Hugging Face en la Entrega 1 (`miguel-mxrxra04/multimodal-climate-change-2008-2026`): una observación por semana con la entradilla vigente en esa fecha y series numéricas (CO2, Brent, anomalía de temperatura, CH4, N2O, índice ONI y volumen mediático de GDELT). Esta entrega prepara y limpia ese dataset y construye indicadores básicos (volumen, sentimiento, tópicos y palabras clave) que permiten formular y contrastar una hipótesis.

## 2. Preguntas de investigación e hipótesis

**Pregunta general.** ¿Cambia la entradilla de forma sistemática cuando ocurren eventos externos relevantes?

**Hipótesis (única).** En el mes de publicación de un informe del IPCC y en los dos siguientes, la entradilla incorpora más términos con un aumento súbito de frecuencia ("términos en auge") que en el resto de meses. La hipótesis nula es que no hay diferencia.

**Resultado.** No se rechaza la hipótesis nula. En los 28 meses post-IPCC hay más términos en auge que en el resto (media de 4,14 frente a 2,49; mediana de 1 frente a 0), pero la diferencia de 1,65 términos por mes no es significativa (p = 0,183 con un test de permutación por desplazamiento circular), así que los datos no permiten afirmar que los informes del IPCC provoquen más cambios en el texto.

**Otras observaciones.** Al quitar la tendencia (variaciones mes a mes), ni el sentimiento ni los tópicos ni el volumen de revisiones se relacionan con CO2, temperatura, ONI o Brent (|r| <= 0,20). En niveles aparecen correlaciones altas (p. ej. sentimiento frente a CO2, -0,68) que se deben a que las series comparten una tendencia a lo largo de los años, no a una relación real.

## 3. Justificación del dataset y de los indicadores

### Dataset

- Es **multimodal y temporal**: combina texto (la entradilla) con series numéricas alineadas por semana, lo que permite comparar cómo cambia el texto con señales externas.
- Conserva la **historia del texto**: una revisión de Wikipedia por semana, de 2008 a 2026 (978 observaciones, 376 textos distintos tras la limpieza).
- Procede de **fuentes públicas** (API de Wikipedia/MediaWiki, NOAA, NASA GISTEMP, Yahoo Finance y GDELT) y es reproducible.
- Solo contiene la **entradilla**, no el artículo completo; se mantuvo así por tamaño y por ser el resumen más estable del artículo, pero limita el análisis (ver apartado 4).

### Indicadores obligatorios

- **Volumen temporal.** El dataset guarda una sola revisión por semana, así que no sirve para contar publicaciones. Se descargó el historial completo de revisiones del artículo (13.469 revisiones) y se contó por semana y por mes. Mide la actividad editorial: media de 13,8 revisiones por semana, mediana de 7 y máximo de 152.
- **Sentimiento medio agregado.** El enunciado pide un modelo en español y los textos están en inglés, así que se tradujeron frase a frase (`Helsinki-NLP/opus-mt-en-es`) y se aplicó `pysentimiento/robertuito-sentiment-analysis`. Se eligió frente a BETO porque devuelve probabilidades graduadas, que se pueden promediar por mes. El tono es neutro o negativo (84 % de las semanas neutras, 16 % negativas, ninguna positiva) y se vuelve más negativo con los años (de -0,20 de media en 2008 a -0,42 en 2023).
- **Distribución de tópicos.** LDA (gensim) con 5 tópicos, entrenado sobre las frases únicas (cada texto es la media ponderada de sus frases), con coherencia c_v ≈ 0,44. Se eligió LDA y no BERTopic por el pequeño número de textos casi idénticos. Los tópicos cambian de foco con los años: emisiones y límites domina en 2012-2013 (0,60 y 0,54) y energía y combustibles fósiles sube hasta 0,37 en 2022.

### Indicador opcional

- **Palabras clave** (términos cuya frecuencia aumenta súbitamente). Se comparó la frecuencia de cada término en las 12 semanas siguientes y en las 12 anteriores, y se marcó como "en auge" si aparece al menos 3 veces por 1.000 palabras y su frecuencia se multiplica por 3 o más. Resultado: 594 de 1.011 términos; 393 aparecen por primera vez y 201 reaparecen. Los saltos se concentran en pocos periodos (2011 y 2019-2022), cuando la entradilla se reescribe, así que el indicador funciona como detector de reescrituras. Se eligió frente a la diversidad léxica (casi constante en textos de estilo parecido), la similitud semántica (repite lo que ya sabemos: el 62 % de las semanas repite el texto anterior) y la clasificación con LLM (coste y criterio subjetivo).

Con los cuatro indicadores y las series numéricas se construyó una tabla mensual (`data/processed/indicadores_mensual.csv`) que es la base de la hipótesis.

## 4. Limitaciones y posibles sesgos

**Datos**
- Un único artículo y solo su entradilla, en inglés: texto enciclopédico y neutro. No refleja la opinión pública ni la cobertura de los medios, y hereda el sesgo de la comunidad editora de Wikipedia en inglés.
- Mucha repetición: el 62 % de las semanas repite un texto ya visto (42 % antes de limpiar el formato). Las 978 semanas no son observaciones independientes; hay solo 376 textos distintos.
- Temperatura, CH4, N2O y ONI son series mensuales repetidas en las semanas de cada mes (cambian solo en el 22-23 % de las semanas). `media_volume_norm` (GDELT) es un proxy, casi siempre cercano a 0.
- La ficha de Hugging Face indica 977 registros y el dataset tiene 978.

**Indicadores**
- Sentimiento: traducción automática más un modelo entrenado con tuits. Mide el tono del contenido (riesgos, consecuencias), no una opinión, y casi no varía.
- Tópicos: pocas frases muy parecidas, con tópicos que comparten vocabulario (uno de ellos domina en solo 3 textos). Son orientativos; la proporción de cada tópico cambia con las versiones de la entradilla.
- Volumen: incluye ediciones de bots y reversiones, es del artículo completo y no solo de la entradilla, y tiene picos puntuales sin explicar.
- Palabras clave: cada término conserva un único salto, no se pueden evaluar las primeras y últimas 12 semanas y el resultado depende de los parámetros. Un salto indica cuándo cambia el texto, no por qué.

**Hipótesis**
- Solo 28 meses post-IPCC (11 informes, con ventanas que se solapan): poca potencia estadística.
- Las fechas de los informes AR5 y SR1.5 no están verificadas y se dejaron fuera los informes especiales de 2011 (SRREN y SREX), año con más reescrituras.
- Una asociación entre un informe y una reescritura no implica causalidad; otros eventos (acuerdos, conferencias del clima) o la propia dinámica de edición pueden explicarla.
