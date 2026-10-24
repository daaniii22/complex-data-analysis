# 1. Introducción y Formulación de la Investigación

## 1.1 Motivación y Contexto Académico
El análisis contemporáneo del cambio climático enfrenta una fragmentación metodológica estructural: mientras las disciplinas científicas monitorizan la degradación del planeta mediante variables cuantitativas continuas (partes por millón de gases de efecto invernadero, anomalías térmicas y dinámicas de precios energéticos), las ciencias sociales y computacionales rastrean la percepción colectiva a través de medios masivos o enciclopedias abiertas. Esta investigación aborda el problema de la **dinámica temporal multivariada en sistemas complejos**, articulando tres dimensiones heterogéneas:

1. **Señales Biofísicas y Macroeconómicas (Real-World Signals):** Concentración troposférica de $CO_2$, $CH_4$, $N_2O$, índice oceánico El Niño (ONI), anomalías térmicas globales (NASA GISTEMP) y el precio de los futuros de petróleo crudo Brent[cite: 1].
2. **Atención Mediática Internacional (Media Exposure):** Intensidad relativa semanal de la agenda de prensa global extraída del repositorio GDELT (Global Database of Events, Language, and Tone).
3. **Consenso Epistémico y Discurso Público (Collaborative Narrative):** Trayectoria y velocidad de mutación semántica del artículo canónico *Climate change* en la Wikipedia en inglés a lo largo del periodo 2008–2026[cite: 1].

El núcleo del proyecto radica en dilucidar si las narrativas públicas compartidas evolucionan en sintonía con las perturbaciones climáticas y económicas reales, o si su transformación está desacoplada de la física atmosférica y supeditada a ondas de choque causadas por la atención de los medios de comunicación masivos.

---

## 1.2 Formulación Formal de la Investigación

* **Título Propuesto:**  
  *«Análisis de Acoplamiento y Dinámica Temporal entre Señales Físico-Económicas, Atención Mediática y Narrativa Colaborativa en Torno al Cambio Climático (2008–2026)»*[cite: 1]

* **Pregunta de Investigación ($Q$):**  
  *¿Es la evolución semántica del discurso público (Wikipedia) una respuesta rezagada (lagged) a las anomalías climáticas y de mercado, o está Granger-causada primordialmente por picos exógenos en la agenda mediática global (GDELT)?*

---

## 1.3 Marco de Hipótesis Operativas

Para responder a la pregunta de investigación sin incurrir en correlaciones espurias, se someten a contraste dos hipótesis estadísticas sobre series temporales estacionarias y diferenciadas ($\Delta X_t$):

* **$H_1$ — Hipótesis de Inercia Estructural (Desacoplamiento Biofísico):**  
  Las fluctuaciones periódicas en los indicadores climáticos continuos ($CO_2$, anomalías térmicas) no contienen información estadística predictiva para anticipar la velocidad de cambio semántico ($\Delta S_t$) del corpus enciclopédico:
  $$\mathcal{F}_{\Delta S_t \mid \mathcal{I}_{t-1}} = \mathcal{F}_{\Delta S_t \mid \mathcal{I}_{t-1} \setminus \{\mathbf{X}_{\text{físico}}\}} \quad \implies \quad p\text{-valor (Granger)} > 0.05$$
  *Racionalidad:* Las modificaciones conceptuales del artículo central no reaccionan al incremento paulatino de los gases, reflejando una inercia institucional en el conocimiento consolidado.

* **$H_2$ — Hipótesis de Mediación por Shock Mediático y Macroeconómico:**  
  Los incrementos abruptos en el volumen de cobertura mediática (GDELT) o las oscilaciones críticas en el coste del combustible fósil (Brent) Granger-causan aumentos en la tasa de reescritura semántica ($\Delta S_t$) de la narrativa pública, con una ventana de rezago estricta $\tau \in [1, 4]$ semanas[cite: 1]:
  $$\text{Var}\left(\epsilon_{\Delta S_t} \mid \mathcal{I}_{t-1}\right) < \text{Var}\left(\epsilon_{\Delta S_t} \mid \mathcal{I}_{t-1} \setminus \{\text{GDELT}_{t-\tau}, \text{Brent}_{t-\tau}\}\right) \quad \text{para algún } \tau \in [1, 4]$$
  *Racionalidad:* Los eventos geopolíticos o comunicativos de alto impacto actúan como catalizadores exógenos que polarizan o actualizan el resumen enciclopédico de forma inmediata.

---

## 1.4 Aportación Metodológica en Descubrimiento de Conocimiento
El marco técnico implementa principios de datos **FAIR** (Findable, Accessible, Interoperable, Reusable), garantizando:
* Erradicación de **Look-Ahead Bias** mediante desfases deliberados de publicación en variables mensuales ($M \to M+1$).
* Modelado continuo y uniforme mediante un índice sintético semanal ($\Delta t = 7\text{ días}$).
* Conversión de cadenas textuales no estructuradas en representaciones densas mediante sentence embeddings para construir la serie derivada de velocidad semántica:
  $$\Delta S_t = 1 - \frac{\mathbf{e}_t \cdot \mathbf{e}_{t-1}}{\|\mathbf{e}_t\| \|\mathbf{e}_{t-1}\|}$$
  analizable mediante modelos VAR (Vector Autoregression) y tests de causalidad en el dominio temporal.