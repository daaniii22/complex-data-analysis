# **Análisis Temporal y Contraste de Hipótesis — Entrega 3**

**Proyecto:** Evolución temporal del artículo de Wikipedia *Climate change* (2008–2026) y su relación con series climáticas, económicas y publicaciones del IPCC.  
**Notebook:** [`notebooks/3_temporal_analysis.ipynb`](notebooks/3_temporal_analysis.ipynb)  
**Resultados (gráficos y tablas):** carpeta [`results/`](results/)

---

## **1. Hipótesis retomada de la Entrega 2 y fechas del IPCC**

Partimos de la hipótesis que definimos en la Entrega 2 (`motivation.md`):

- **Hipótesis ($H_1$):** *En el mes de publicación de un informe del IPCC y en los dos siguientes ($K = 3$ meses), la entradilla del artículo Climate change de Wikipedia en inglés incorpora **más términos en auge** que en el resto de meses.*
- **Hipótesis nula ($H_0$):** *No hay diferencia positiva en el número de términos en auge entre los meses posteriores a un informe del IPCC y el resto.*

En la Entrega 2 dejamos pendientes dos comprobaciones que cerramos aquí (`results/eventos_ipcc_verificados.csv`):
1. **Confirmación de fechas:** verificamos las fechas oficiales de **AR5** (`2013-09-27`, `2014-03-31`, `2014-04-12`, `2014-11-02`) y **SR1.5** (`2018-10-08`), que coinciden con los meses que usamos en la Entrega 2.
2. **Escenarios con los informes especiales de 2011:** como 2011 tuvo muchos cambios en el texto, probamos tres calendarios distintos:
   - **Entrega 2 original (`11 informes`, 2013–2023):** ciclos AR5, SR1.5, SRCCL, SROCC y AR6 (`28` meses en ventana post-IPCC con $K = 3$).
   - **Ampliado 2011 con SREX SPM (`13 informes`):** suma **SRREN** (`2011-05-09`) y el resumen para responsables de políticas de **SREX** (`2011-11-18`), con `34` meses post-IPCC.
   - **Ampliado 2011 con SREX Completo (`13 informes`):** suma **SRREN** (`2011-05-09`) y la salida del informe completo de **SREX** (`2012-03-28`), también con `34` meses post-IPCC.

**Informes del IPCC incluidos** (`results/eventos_ipcc_verificados.csv`):

| Informe | Fecha | Escenario |
|---|---|---|
| AR5 — Grupo de trabajo I | `2013-09-27` | los 11 (E2 original) y los 13 |
| AR5 — Grupo de trabajo II | `2014-03-31` | los 11 y los 13 |
| AR5 — Grupo de trabajo III | `2014-04-12` | los 11 y los 13 |
| AR5 — Informe de síntesis | `2014-11-02` | los 11 y los 13 |
| SR1.5 — Calentamiento de 1,5 °C | `2018-10-08` | los 11 y los 13 |
| SRCCL — Cambio climático y tierra | `2019-08-07` | los 11 y los 13 |
| SROCC — Océano y criosfera | `2019-09-25` | los 11 y los 13 |
| AR6 — Grupo de trabajo I | `2021-08-09` | los 11 y los 13 |
| AR6 — Grupo de trabajo II | `2022-02-28` | los 11 y los 13 |
| AR6 — Grupo de trabajo III | `2022-04-04` | los 11 y los 13 |
| AR6 — Informe de síntesis | `2023-03-20` | los 11 y los 13 |
| SRREN — Energías renovables | `2011-05-09` | solo los 13 (ambas variantes) |
| SREX — Eventos extremos (SPM) | `2011-11-18` | solo los 13 con SREX SPM |
| SREX — Eventos extremos (informe completo) | `2012-03-28` | solo los 13 con SREX Completo |

---

## **2. Mejoras tras el feedback de la Entrega 2**

### **2.1. Indicador multi-periodo de términos en auge (`terminos_en_auge_multi`)**

En la Entrega 2 (`palabras_clave_auge.csv`), cada palabra solo guardaba la semana de su **mayor subida** (`puntuacion.argmax(axis=0)`), dejando fuera otros momentos en los que volvía a ganar peso. Siguiendo el comentario del profesor, en la Sección 1.1 de `3_temporal_analysis.ipynb` cargamos en solo lectura `data/processed/dataset_clean.parquet` y `data/processed/textos_unicos.parquet` y reprodujimos exactamente el preprocesado y los umbrales originales (`en_core_web_sm`, misma lista de stopwords, lemas alfabéticos $> 2$ letras, `CountVectorizer(min_df=3)`, frecuencia por 1.000 palabras proyectada a 978 semanas vía `text_id`, `VENTANA = 12`, `FREC_MIN = 3.0`, `RATIO_MIN = 3.0`, obteniendo de nuevo los 594 términos de la Entrega 2).

A partir de ahí, localizamos todas las semanas donde `despues >= 3.0` y `log2_ratio >= log2(3.0)` y **agrupamos las semanas consecutivas en episodios contiguos distintos**, para no contar varias veces el mismo salto por el solapamiento de la ventana móvil de 12 semanas. En cada episodio elegimos la semana con mayor `log2_ratio` (desempatando por la primera) y guardamos los resultados en `results/palabras_clave_auge_multiperiodo.csv` y `results/palabras_clave_mensual_multiperiodo.csv`.

| Métrica | Entrega 2 original (`terminos_en_auge_e2`) | Multi-periodo (`terminos_en_auge_multi`) |
|---|---:|---:|
| Total de episodios | 594 | **816** (+222; +37,4 %) |
| Términos únicos | 594 | 594 |
| Términos con $> 1$ episodio | 0 | **165** (máximo 4 episodios) |
| Media mensual (225 meses) | 2,640 | **3,627** |
| Mediana mensual | 0,0 | 0,0 |
| Meses en cero | 60,0 % | **57,3 %** |
| Máximo mensual (`mes`) | 36 (`2020-09`) | **45** (`2020-09`) |

**Ejemplo de `adaptation`:** en la Entrega 2 solo salía en `2023-04-23` (salto `17,74`, `log2_ratio = 5,19`). Con `terminos_en_auge_multi` recogemos sus **4 subidas**: `2009-02` (primera aparición, salto `5,17`, 9 semanas), `2011-01` (salto `6,03`, 9 semanas), `2021-01` (salto `10,84`, 12 semanas) y `2023-04` (salto `17,74`, 13 semanas, tras el Informe de Síntesis de AR6).

### **2.2. Diagnóstico de baja unicidad del texto (< 50 % único)**

Para analizar el aviso del profesor sobre la repetición del texto (`results/diagnostico_unicidad_textual.csv`), revisamos `text_id` y `texto_nuevo` a lo largo de las 978 semanas:

- **Textos únicos:** `376` de `978` semanas (**38,45 %**, por debajo del 50 %).
- **Semanas sin cambio:** `598` de `978` (**61,15 %**; solo `380` semanas cambian respecto a la anterior).
- **Meses sin ningún cambio:** `44` de `225` meses (**19,56 %**) transcurren sin tocar la entradilla.
- **Rachas de texto idéntico:** media de `2,57` semanas, mediana de `1,0`, percentil 75 de `3,0`, percentil 90 de `6,0` y máximo de **`24` semanas seguidas**.

Como el texto permanece igual durante varias semanas o meses, `sent_medio` y `topico_0..4` se comportan en escalón y muestran una autocorrelación parcial en lag 1 muy cercana a 1 (`PACF(1) = 0,9665` en `sent_medio` y entre `0,9452` y `0,9815` en `topico_0..4`), frente a valores mucho menores en `revisiones_total` (`0,5884`) y `terminos_en_auge_multi` (`0,2484`). Esto explica por qué `Naive (t-1)` consigue errores tan bajos a 1 paso en `sent_medio`. Por ello trabajamos en **frecuencia mensual** y nos apoyamos sobre todo en `revisiones_total` y `terminos_en_auge_multi`.

---

## **3. Técnicas aplicadas**

1. **Exploración temporal (Sección 2):**
   - Estacionariedad con el test **ADF** en niveles y en primeras diferencias.
   - Autocorrelación con **Ljung-Box** (retardos 1 y 12) y gráficos **ACF/PACF** (24 meses).
   - Estacionalidad mensual con **Kruskal-Wallis** por mes del año y descomposición aditiva (periodo 12).
   - Tendencia con el filtro **Hodrick-Prescott** ($\lambda = 129.600$).
2. **Contraste de hipótesis (Sección 3, `2008-04`..`2026-06`, 219 meses):**
   - **Test de permutación circular** (respeta la autocorrelación y la agrupación de informes) en los 3 calendarios IPCC y con $K \in \{1, 2, 3, 4\}$, comparando `terminos_en_auge_multi` (principal) y `terminos_en_auge_e2` (original).
   - **Perfil de rezagos** ($\tau \in [-3, +5]$ meses alrededor de cada informe) y revisión directa del texto en `2011-11`.
   - **Modelos SARIMAX con intervención (`post_ipcc`)**, controlando por ARMA(1,0,0) y por `log1p(revisiones_total)`. Como SARIMAX supone errores normales —lo cual limita su uso en conteos con 57,3 % de ceros—, estimamos todos los modelos también sobre `log1p(...)` y los contrastamos con la permutación circular.
3. **Modelado predictivo (Sección 4):**
   - Partición cronológica estricta y selección de órdenes SARIMA por AIC solo en entrenamiento:
     - `revisiones_total` (sobre `log1p`) y `sent_medio`: test de 24 meses completos (`2024-09`..`2026-08`) en modos **1 paso adelante** y **multi-paso (24m)**, más proyección de 12 meses (`2026-09`..`2027-08`) con los órdenes ganadores reentrenados sobre toda la serie.
     - `terminos_en_auge_multi`: test de 48 meses (`2021-01`..`2024-12`, todo el ciclo AR6) comparando SARIMA sin exógena, SARIMAX con `post_ipcc_11` / `post_ipcc_13_spm` (niveles y `log1p`), Suavizado Exponencial (**SES** y **Holt amortiguado**), **RNN/LSTM** en PyTorch y baselines (`Naive`, `Naive estacional`, `Media histórica`, `Cero constante`).
   - Métricas **MAE** y **RMSE**, y comprobación de ruido blanco en residuos con **Ljung-Box (`lag = 12`)**.
4. **Técnicas adicionales (Sección 5):**
   - **Detección de anomalías** con Z-score basado en **MAD** sobre los residuos de `SARIMAX(1,0,0)` en `log1p(terminos_en_auge_multi)`, con umbral **$Z_{\text{MAD}} > 4{,}0$**.
   - **Comparación de periodos** (`2008–2012`, `2013–2018`, `2019–2022`, `2023–2026`) mediante Kruskal-Wallis.

---

## **4. Resultados y visualizaciones**

### **4.1. Exploración temporal, estacionariedad y estacionalidad**

- **Figura 1:** [`results/01_evolucion_indicadores_y_periodos.png`](results/01_evolucion_indicadores_y_periodos.png) — Evolución mensual de los 4 indicadores, tendencia Hodrick-Prescott, periodos históricos y fechas del IPCC.
- **Figura 2:** [`results/02_descomposicion_acf_pacf.png`](results/02_descomposicion_acf_pacf.png) — Tendencia (media móvil 12m), ACF y PACF de `terminos_en_auge_multi`, `revisiones_total` y `sent_medio`.

| Serie | Media | Mediana | % Ceros | ADF `p` (nivel) | ADF `p` ($\Delta^1$) | LB `p` (lag 1) | KW estac. `p` | Fuerza estac. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `terminos_en_auge_multi` | 3,627 | 0,000 | 57,3 % | **0,0105** | 0,0000 | 0,0002 | 0,8053 | 0,038 |
| `terminos_nuevos_multi` | 1,920 | 0,000 | 64,9 % | **0,0002** | 0,0000 | 0,0001 | 0,7986 | 0,036 |
| `revisiones_total` | 59,862 | 35,000 | 0,0 % | 0,4541 | **0,0000** | 0,0000 | 0,9826 | 0,023 |
| `sent_medio` | -0,285 | -0,315 | 0,0 % | 0,1691 | **0,0000** | 0,0000 | 0,9999 | 0,068 |
| `co2_ppm` (referencia) | 406,517 | 406,793 | 0,0 % | 0,9875 | **0,0054** | 0,0000 | 0,9291 | **0,982** |

- Ningún indicador del artículo tiene estacionalidad anual (`KW p ≥ 0,798`, fuerza estacional `≤ 0,068`).

### **4.2. Contraste de hipótesis: permutación circular, rezagos y SARIMAX**

- **Figura 3:** [`results/03_contraste_hipotesis_ipcc.png`](results/03_contraste_hipotesis_ipcc.png) — Media de episodios antes y después de cada informe ($\tau \in [-3, +5]$) y distribución nula de la permutación circular ($K = 3$).

**Permutación circular ($K = 3$ meses, 219 meses evaluables; `results/contraste_hipotesis_ipcc.csv`):**

| Indicador | Escenario IPCC | $n_{\text{post}}$ | Media post | Media resto | Mediana post / resto | $\Delta$ medias | $p_{\text{perm}}$ |
|---|---|---:|---:|---:|---:|---:|---:|
| **Multi-periodo (principal)** | **11 informes (E2 original, 2013–2023)** | 28 | 6,071 | 3,372 | 1,5 / 0,0 | +2,700 | **0,1324** |
| **Multi-periodo (principal)** | 13 informes (SREX SPM nov-2011) | 34 | 7,559 | 3,011 | 2,0 / 0,0 | +4,548 | **0,0137** |
| **Multi-periodo (principal)** | 13 informes (SREX Completo mar-2012) | 34 | 6,118 | 3,276 | 1,5 / 0,0 | +2,842 | **0,1142** |
| Entrega 2 (comparativa) | 11 informes (E2 original, 2013–2023) | 28 | 4,143 | 2,492 | 1,0 / 0,0 | +1,651 | 0,1826 |
| Entrega 2 (comparativa) | 13 informes (SREX SPM nov-2011) | 34 | 5,529 | 2,184 | 1,5 / 0,0 | +3,346 | 0,0137 |
| Entrega 2 (comparativa) | 13 informes (SREX Completo mar-2012) | 34 | 4,353 | 2,400 | 1,0 / 0,0 | +1,953 | 0,1279 |

**Modelos SARIMAX con intervención (`results/sarimax_intervencion_hipotesis.csv`):**

| Serie objetivo | Modelo | $\beta_{\text{IPCC}}$ | $p_{\text{IPCC}}$ | $\beta_{\log(\text{rev})}$ ($p$) | AIC | BIC | LB res. `p` (lag 12) |
|---|---|---:|---:|---:|---:|---:|---:|
| `terminos_en_auge_multi` | ARMA(1,0,0) (sin exógena) | — | — | — | 1503,63 | 1513,79 | 0,0049 |
| `terminos_en_auge_multi` | SARIMAX(1,0,0) + `post_ipcc_11` | +2,7564 | 0,0978 | — | 1503,12 | 1516,67 | 0,0055 |
| `terminos_en_auge_multi` | SARIMAX(1,0,0) + `post_ipcc_11` + `log_rev` | +2,6025 | 0,0555 | +3,4692 (0,0000) | 1465,67 | 1482,62 | 0,1219 |
| `terminos_en_auge_multi` | SARIMAX(1,0,0) + `post_ipcc_13_spm` | +4,2620 | 0,0010 | — | 1498,39 | 1511,95 | 0,0053 |
| `terminos_en_auge_multi` | SARIMAX(1,0,0) + `post_ipcc_13_full` | +2,6554 | 0,0962 | — | 1502,85 | 1516,41 | 0,0138 |
| `log1p(auge_multi)` | ARMA(1,0,0) (sin exógena) | — | — | — | 638,00 | 648,17 | 0,0069 |
| `log1p(auge_multi)` | SARIMAX(1,0,0) + `post_ipcc_11` | +0,3437 | 0,1372 | — | 638,18 | 651,73 | 0,0074 |
| `log1p(auge_multi)` | SARIMAX(1,0,0) + `post_ipcc_11` + `log_rev` | +0,3561 | 0,0432 | +0,5750 (0,0000) | **587,54** | **604,49** | **0,8278** |
| `log1p(auge_multi)` | SARIMAX(1,0,0) + `post_ipcc_13_spm` | +0,5234 | 0,0124 | — | 634,97 | 648,53 | 0,0074 |
| `log1p(auge_multi)` | SARIMAX(1,0,0) + `post_ipcc_13_full` | +0,3534 | 0,1056 | — | 637,69 | 651,25 | 0,0140 |
| `log1p(auge_e2)` (comp.) | SARIMAX(1,0,0) + `post_ipcc_11` | +0,3043 | 0,1489 | — | 590,53 | 604,09 | 0,0043 |
| `log1p(revisiones)` | SARIMAX(1,0,1) + `post_ipcc_11` | +0,0459 | 0,7872 | — | 505,97 | 522,92 | 0,7268 |

### **4.3. Modelos predictivos y pronóstico (`2026-09`..`2027-08`)**

- **Figura 4:** [`results/04_modelos_pronostico_revisiones.png`](results/04_modelos_pronostico_revisiones.png) — Predicción en test (24m) y proyección futura (`2026-09`..`2027-08`) para `revisiones_total` y `sent_medio`.
- **Figura 5:** [`results/05_sarimax_hipotesis_y_auge.png`](results/05_sarimax_hipotesis_y_auge.png) — Pronóstico sobre `terminos_en_auge_multi` en el ciclo AR6 (`2021–2024`) y ACF de residuos de `SARIMAX(1,0,0) + post_ipcc_11`.

**Métricas fuera de muestra (`results/metricas_modelos_temporales.csv`):**

| Serie | Horizonte | Modelo | MAE | RMSE |
|---|---|---|---:|---:|
| `revisiones_total` | 1-paso adelante | **SARIMA (0,1,1)×(1,0,0,12)** (`log1p`) | **15,1603** | **23,6397** |
| `revisiones_total` | 1-paso adelante | RNN (LSTM PyTorch) | 18,8057 | 27,8937 |
| `revisiones_total` | 1-paso adelante | Baseline Naive ($t-1$) | 21,2917 | 33,0221 |
| `revisiones_total` | Multi-paso (24m) | Baseline Naive (último valor) | **15,7500** | **23,7785** |
| `revisiones_total` | Multi-paso (24m) | SARIMA (0,1,1)×(1,0,0,12) (`log1p`) | 18,9588 | 25,0564 |
| `revisiones_total` | Multi-paso (24m) | Suavizado Exponencial (SES) | 19,2607 | 25,2221 |
| `revisiones_total` | Multi-paso (24m) | Suavizado Holt amortiguado | 19,4396 | 25,3032 |
| `revisiones_total` | Multi-paso (24m) | RNN (LSTM PyTorch) | 28,2776 | 36,7328 |
| `revisiones_total` | Multi-paso (24m) | Baseline Media histórica | 46,9619 | 48,3659 |
| `sent_medio` | 1-paso adelante | Baseline Naive ($t-1$) | **0,0042** | 0,0082 |
| `sent_medio` | 1-paso adelante | **SARIMA (1,0,0)** | 0,0043 | **0,0078** |
| `sent_medio` | 1-paso adelante | RNN (LSTM PyTorch) | 0,0046 | 0,0081 |
| `sent_medio` | Multi-paso (24m) | **SARIMA (1,0,0)** | **0,0206** | **0,0228** |
| `sent_medio` | Multi-paso (24m) | RNN (LSTM PyTorch) | 0,0288 | 0,0303 |
| `sent_medio` | Multi-paso (24m) | Suavizado Exponencial (SES) / Naive últ. | 0,0415 | 0,0435 |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | SARIMAX (1,0,0) + `post_ipcc_13_spm` | 5,5707 | **8,5512** |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | SARIMAX (1,0,0) + `post_ipcc_11` | 5,6025 | 8,5734 |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | Baseline Media entrenamiento | 5,5739 | 8,6457 |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | SARIMA (1,0,0) (sin exógena) | 5,5831 | 8,6828 |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | SARIMAX (1,0,0) `log1p` + `post_ipcc_11` | 4,7130 | 9,1179 |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | RNN (LSTM PyTorch) | 4,9337 | 9,4875 |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | Suavizado Exponencial (SES) | 8,3412 | 9,5784 |
| `terminos_en_auge_multi` | Multi-paso AR6 (48m) | Baseline Cero constante | **4,6458** | 9,7820 |

- **Residuos (`Ljung-Box lag = 12`):** `revisiones_total` (`p = 0,7092` en train; `stat = 9,947`, `p = 0,6206` en toda la serie) y `sent_medio` (`p = 0,6051` en train; `stat = 11,099`, `p = 0,5204` en toda la serie) se comportan como ruido blanco. En `terminos_en_auge_multi`, `SARIMAX(1,0,0) + post_ipcc_11` rechaza ruido blanco (`p = 0,0055` en niveles; `p = 0,0074` en `log1p`).
- **Pronóstico futuro (`2026-09`..`2027-08`, `results/pronostico_futuro_12m.csv`):** se mantiene un volumen bajo (`~12,35–12,37` revisiones/mes, IC 95 % de `[2,05; 57,56]` en `2026-09` a `[1,03; 86,81]` en `2027-08`) y un sentimiento estable en torno a `-0,3235` a `-0,3163`.

### **4.4. Anomalías y comparación de periodos**

- **Figura 6:** [`results/06_deteccion_anomalias_y_regimenes.png`](results/06_deteccion_anomalias_y_regimenes.png) — Meses anómalos ($Z_{\text{MAD}} > 4{,}0$) dentro y fuera de las ventanas del IPCC y medias por periodo.
- **Anomalías (`results/anomalias_detectadas.csv`):** encontramos **16 meses anómalos de 219 (`7,3 %`)**. Solo **5 (`31,2 %`)** están en ventanas de los 11 informes IPCC (`2021-10`, `2019-11`, `2014-12`, `2019-09`, `2022-05`); los otros **11 (`68,8 %`)** caen fuera, incluidos los dos mayores picos de toda la serie, sin relación con el IPCC: `2020-09` (45 episodios, 301 rev.: `health, warm, result`) y `2020-03` (43 episodios, 212 rev.: `impact, development, technology`). Otros picos fuera de las ventanas de los 11 informes son `2011-11` (37 episodios; solo cae en la ventana del escenario `13_spm` y se explica por citas del AR4, ver sección 5) y `2021-01` (32 episodios, 221 rev.: `adaptation, risk, people`).
- **Periodos históricos (Kruskal-Wallis, `results/comparacion_periodos.csv`):** las cuatro etapas difieren claramente en `terminos_en_auge_multi` ($H = 40,26$, $p = 9,37 \times 10^{-9}$), `revisiones_total` ($H = 80,29$, $p = 2,66 \times 10^{-17}$) y `sent_medio` ($H = 98,52$, $p = 3,23 \times 10^{-21}$).

| Periodo | Meses | Rev. media (med.) | Episodios/mes (total) | Sent. medio | T0 | T3 | T4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `2008–2012 (AR4 / SRREN-SREX)` | 60 | 91,5 (84,0) | 4,55 (273) | -0,215 | 0,128 | 0,333 | 0,147 |
| `2013–2018 (Ciclo AR5 / SR1.5)` | 72 | 28,7 (21,5) | 1,39 (100) | -0,261 | 0,162 | **0,408** | 0,087 |
| `2019–2022 (SRs + Ciclo AR6)` | 48 | **95,8** (66,0) | **8,21 (394)** | -0,337 | 0,304 | 0,136 | 0,230 |
| `2023–2026 (Post-AR6)` | 45 | 29,3 (24,0) | 1,09 (49) | **-0,362** | **0,316** | 0,222 | **0,301** |

---

## **5. Discusión: hipótesis apoyada o refutada**

**Veredicto: la hipótesis $H_1$ queda refutada (no podemos rechazar $H_0$).**

Aunque pasar al indicador multi-periodo (`terminos_en_auge_multi`) recupera 222 episodios y sube la diferencia media en los 11 informes base de `+1,651` a `+2,700` episodios/mes, los datos siguen sin respaldar una relación general con el calendario del IPCC:

1. **Los tests no salen significativos ni en el calendario base ni con SREX Completo:** la permutación circular da `p = 0,1324` (11 informes) y `p = 0,1142` (13 informes con SREX Completo), igual que SARIMAX sin controles (`p = 0,0978` en niveles; `p = 0,1372` en `log1p`). El volumen de revisiones tampoco cambia tras los informes (`p = 0,7872`).
2. **El único escenario significativo (`13_spm`, `p = 0,0137`) es una coincidencia de fechas:** ese resultado depende de meter `2011-11` (37 episodios) en la ventana del SREX SPM (`2011-11-18`). Al mirar `dataset_clean.parquet`, comprobamos que los cambios de noviembre de 2011 arrancaron el **`2011-11-06` y el `2011-11-13` (hasta 12 días antes del SREX)** y las palabras en auge (`synthesis`, `section`, `uncertainty`, `projections`, `chap`, `meehl`) corresponden a citas del **AR4 (2007)**, no del SREX.
3. **No mejora la predicción fuera de muestra:** en el ciclo AR6 (`2021–2024`), incluir `post_ipcc_11` en `SARIMAX(1,0,0)` apenas baja el RMSE un `1,3 %` respecto a `SARIMA(1,0,0)` sin exógena (`8,5734` vs. `8,6828`) y no mejora el MAE (`5,6025` vs. `5,5831`).
4. **Matiz importante:** sí vemos respuestas concretas al mes siguiente ($\tau = +1$) de algunos informes, sobre todo `SROCC 2019` (`acidification, ocean`) y `AR6 WGI 2021` (`adapt, forest, action`), y al controlar por `log_rev` en `log1p` el coeficiente de `post_ipcc_11` solo llega a ser significativo al 5 % en `log1p` (`p = 0,0432`; en niveles, `p = 0,0555`). Sin embargo, casi siete de cada diez meses anómalos (`68,8 %`) —y los dos mayores picos de toda la serie (`2020-09` y `2020-03`)— se deben a **reescrituras internas de Wikipedia**, no a las fechas del IPCC.

---

## **6. Limitaciones y posibles mejoras**

### **Limitaciones**
- **Poca unicidad del texto (< 50 %):** solo el `38,45 %` de las semanas tiene texto único y el `19,56 %` de los meses no cambia nada, lo que infla la autocorrelación (`PACF(1) ≈ 0,97`) en sentimiento y tópicos y mantiene el tono enciclopédico casi plano.
- **Exceso de ceros y supuesto gaussiano en SARIMAX:** con un `57,3 %` de ceros en `terminos_en_auge_multi`, los residuos de SARIMAX no cumplen ruido blanco (`LB p = 0,0055`), aunque contrastarlo con `log1p` y permutación circular evita depender solo de ese supuesto.
- **Pocos informes del IPCC:** en 18 años solo hay 11–13 informes, y varios caen muy cerca entre sí (como `SRCCL`/`SROCC` en 2019 o `AR6 WGII`/`WGIII` en 2022), lo que reduce la potencia de los tests.
- **Alcance y causalidad:** analizamos solo la entradilla en inglés y no incluimos otros eventos externos (cumbres COP, noticias de gran impacto o debates internos de Wikipedia) que también pueden provocar reescrituras.

### **Posibles mejoras**
- **Modelos para series de conteo:** sustituir SARIMAX gaussiano por modelos específicos de conteo (**INGARCH Poisson / Binomial Negativa** o modelos **Zero-Inflated**) con regresores de intervención.
- **Analizar el artículo completo:** estudiar el cuerpo entero del artículo (y compararlo con ediciones en otros idiomas), donde las citas de nuevos informes aparecen mucho antes que en la entradilla.
- **Ampliar las señales externas e internas:** incorporar fechas de cumbres **COP**, picos mediáticos y actividad de la página de discusión (*Talk*) de Wikipedia para separar las reescrituras internas de las reacciones a noticias científicas.
