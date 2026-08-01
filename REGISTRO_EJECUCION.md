# Registro de ejecución y decisiones — SimilCode

Documento de trabajo. Recoge todo lo ejecutado y decidido, con la trazabilidad que necesitan la sección de Métodos y la declaración de reproducibilidad. Los campos marcados **[COMPLETAR]** deben rellenarse antes de redactar el manuscrito final.

---

## 1. Benchmark de LLM

**Corpus.** 120 pares controlados, 60 en C# y 60 en Java, balanceados en cuatro categorías de similitud (30 pares por categoría). Definido en `metadata.csv` del repositorio SimilCode-Benchmark.

**Modelos evaluados** (identificadores exactos registrados en la columna `model_snapshot` de cada respuesta):

| Proveedor | Identificador invocado |
|---|---|
| DeepSeek | `deepseek-v4-pro` |
| Google | `gemini-3.1-pro-preview` |
| OpenAI | `gpt-5.5-2026-04-23` |
| Anthropic | `claude-opus-5` |

**Diseño.** Tres réplicas independientes por par y modelo: 120 × 4 × 3 = **1440 evaluaciones**, todas completadas. El acierto de cada par se determina por voto mayoritario de las tres réplicas.

**Temperatura.** Se solicitó 0 en los cuatro proveedores. `claude-opus-5` rechaza ese valor (HTTP 400) por tratarse de un modelo de razonamiento, de modo que sus llamadas se ejecutaron con la temperatura por defecto del proveedor. **Esto debe declararse explícitamente en Métodos.**

**Fechas de recolección.** Del 31 de julio al 1 de agosto de 2026.

**Entornos de ejecución.** La corrida se repartió entre dos equipos, por lo que las latencias absolutas mezclan dos configuraciones. El diseño pareado protege la comparación entre modelos, porque dentro de cada caso los cuatro se ejecutan consecutivamente en la misma máquina; aun así ambos entornos deben describirse.

- Equipo 1: **[COMPLETAR: CPU, RAM, sistema operativo, ancho de banda]** — casos 1 a ~75.
- Equipo 2: **[COMPLETAR: CPU, RAM, sistema operativo, ancho de banda]** — casos restantes.

**Incidencias.** El archivo de resultados contiene 182 filas de reintento además de las 1440 evaluaciones válidas. Se registraron 128 errores HTTP 429 en `gemini-3.1-pro-preview` (límite de cuota del modelo *preview*), resueltos mediante reintentos con espera creciente; 30 errores HTTP 400 en Anthropic por el rechazo de `temperature=0`, resueltos reintentando sin ese parámetro; y 15 errores HTTP 401 en OpenAI por una credencial mal configurada al inicio.

**Prompt.** El archivo `prompt.txt` empleado es una reconstrucción fiel del Apéndice A. **[COMPLETAR: verificar si coincide con el `PROMPT_HASH.txt` original; si no, recalcular el hash SHA-256 del prompt realmente usado y archivarlo.]**

**Datos.** `resultados_replicas.csv` (1622 filas: 1440 evaluaciones válidas + 182 reintentos), archivado en el repositorio.

---

## 2. Validación de la verdad de terreno

Las 120 parejas fueron clasificadas de forma independiente por dos evaluadores: el investigador principal y un segundo docente de programación ajeno a la construcción del conjunto y ciego a las etiquetas originales.

**Acuerdo interevaluador: κ de Cohen = 0.989** (acuerdo observado 99.2 %, 119 de 120 pares).

El único desacuerdo reveló que la variante funcional del grupo CS_010 se había archivado como copia exacta del fragmento idéntico. Se corrigió reemplazando `csharp/CODE_FUN_CS_010.cs` por una reimplementación funcionalmente equivalente (mismo comportamiento y misma salida, implementación distinta). La corrección se aplicó **antes** de que la corrida alcanzara ese caso.

Instrumentos archivados: `categorias_evaluador2.csv` (hoja ciega) y `clave_categorias_ref.csv` (clave, no entregada al evaluador).

---

## 3. Fiabilidad del instrumento de validación con expertos

Calculada sobre `responses/responses_anonymised_wide.csv` del repositorio SimilCode-Validation (5 evaluadores × 18 ítems).

| Subescala | Ítems | α de Cronbach |
|---|---|---|
| Utilidad práctica | Q01–Q07 | 1.000 (degenerado) |
| Exactitud de resultados | Q08–Q13 | 0.933 |
| Comprensibilidad | Q14–Q18 | 0.900 |
| Conjunto de 18 ítems | 18 | 0.661 |

**Patrón de respuesta detectado.** Los cinco evaluadores respondieron un valor constante a lo largo de los siete ítems de la subescala de utilidad, lo que explica el α de 1.000 como artefacto y no como fiabilidad. Tres de los cinco hicieron lo mismo dentro de cada una de las otras dos subescalas. Los ítems Q09 y Q17 no registraron varianza alguna entre participantes.

**Corrección de cifras.** Recalculando desde los datos archivados (promediando primero por evaluador y después entre evaluadores), la subescala de comprensibilidad da **4.60** (el manuscrito indicaba 4.50) y el agregado de los 18 ítems da **4.68 con SD 0.22** (el manuscrito indicaba 4.60 y SD 0.18). Prevalecen los valores derivados de los datos.

---

## 4. Validación del componente Big O

**Corpus.** 40 algoritmos canónicos (20 Java, 20 C#) balanceados en siete clases de complejidad temporal de peor caso, más 8 casos adversariales diseñados para descartar el mero reconocimiento de patrones memorizados (nombres engañosos, anidamiento con cota constante, bucles secuenciales, memoización, código muerto de orden superior).

**Resultado.** 48 de 48 correctos en complejidad temporal y espacial (100 %), con matriz de confusión estrictamente diagonal.

**Convención declarada.** Complejidad temporal de **peor caso**; para el espacio, **espacio auxiliar** (excluye la estructura de entrada, incluye la pila de recursión).

**Corrección de la verdad de terreno.** La primera puntuación arrojó tres discrepancias de espacio; el examen mostró que en los tres casos el error estaba en la verdad de terreno y no en el modelo. Se corrigió `HeapExtractAll` (reserva un arreglo de salida, luego O(n)) y se declaró la convención de espacio auxiliar. La versión previa se conserva como `ground_truth_v1_original.csv`.

**Pendiente.** La clasificación se obtuvo con instancias ciegas de `claude-opus-5` dentro de una sesión asistida, no mediante llamadas directas a la API. **[COMPLETAR: reejecutar `validar_bigo.py` contra la API oficial para registrar el `model_snapshot` y hacer el resultado citable.]**

---

## 5. Hallazgo principal: validez de constructo de la métrica

Los cuatro modelos aplican la fórmula de ponderación prescrita (Funcional 40 %, Estructural 30 %, Léxica 20 %, Estilística 10 %) con fidelidad completa: en el **100 % de las 1435 respuestas** con las cinco dimensiones presentes, el puntaje global reportado coincide con el calculado dentro de ±5 puntos (diferencia media +0.17).

Sin embargo, la banda esperada y la fórmula interactúan con el criterio de superficie de cada modelo. Calculando qué valor debería tener la dimensión funcional para caer dentro de la banda, dadas las demás dimensiones que el propio modelo asignó:

| Modelo | Funcional requerida (categoría funcional) | Observada | Alcanzable |
|---|---|---|---|
| GPT-5.5 | ≥ 86.1 | 94.3 | Sí |
| DeepSeek-V4-pro | ≥ 89.8 | 97.7 | Sí |
| Claude Opus 5 | ≥ 104.5 | 90.7 | **No (supera el máximo de 100)** |
| Gemini 3.1 Pro | ≥ 115.7 | 98.3 | **No (supera el máximo de 100)** |

Gemini y Claude juzgan la similitud superficial de las reimplementaciones con más severidad (Gemini asigna 30.4 de similitud estructural frente a 57.3 de DeepSeek), lectura igualmente defendible que sin embargo les impide alcanzar la banda.

**Consecuencia.** La métrica de coincidencia agregada penaliza a los modelos que evalúan la superficie con mayor rigor, de modo que el ranking de precisión refleja en parte un artefacto de la operacionalización y no solo capacidad de detección. La raíz es que el término «similitud funcional» no se define en el prompt: puede leerse como *propósito de negocio* (Gemini: estudiantes ≠ empleados → 30) o como *patrón computacional* (los demás: listar y clasificar → 65–71).

---

## 6. Comparación con detectores clásicos

**Advertencia de integridad.** Las cifras de Dolos y JPlag que figuraban en versiones previas del manuscrito (53.3 % y 50.8 %, con sus sensibilidades, especificidades y tiempos) **no proceden de ninguna ejecución** y no deben reutilizarse bajo ninguna forma. El repositorio no contiene datos de esas herramientas.

**Protocolo adoptado.** Ejecución en dos modos, reportados por separado: **cohorte** (todas las entregas del lenguaje en una sola corrida, que es el uso real de estas herramientas) y **aislado** (par a par, como suele hacerse en la literatura). La diferencia entre ambos es un resultado reportable.

**Decisiones fijadas a priori:**

- Banda de la categoría *diferente*: **simétrica** (0–20 %, la misma aplicada a los LLM) como resultado principal, y relajada (0–30 %) reportada por transparencia.
- Tolerancia en la categoría *idéntico*: **5 puntos** a la baja, porque su rango es un punto exacto (100–100) y las herramientas de huellas pueden devolver 97–99 para archivos idénticos. Se aplica por igual a todas las herramientas.
- Métrica primaria: `similarity` en Dolos; similitud media en JPlag; media de los dos porcentajes por par en Moss.
- Sin archivo base (`-b`) en ninguna herramienta, en coherencia con el hecho de que SimilCode tampoco excluye plantilla.
- Los pares que Moss no reporta (por debajo de su umbral) se registran como similitud 0.

**Materialización de los pares idénticos.** Como ninguna herramienta compara una entrega consigo misma, se genera una copia con sufijo `_COPY` para que la comparación exista realmente.

### Ejecución de Moss — COMPLETADA

- Servidor: `moss.stanford.edu`, puerto 7690.
- Parámetros registrados por el propio servidor: `-l csharp -d -m 10` y `-l java -d -m 10` (una entrega por directorio, sin archivo base).
- Fecha de ejecución: **1 de agosto de 2026, 04:03 PDT**.
- URLs de resultados (caducan; el HTML descargado queda archivado):
  - C#: `http://moss.stanford.edu/results/7/170698045726/` → `moss_cs.html` (43 090 bytes, 143 comparaciones).
  - Java: `http://moss.stanford.edu/results/9/6676565055708/` → `moss_java.html` (68 412 bytes, 228 comparaciones).

**Cobertura.** De los 120 pares del estudio, Moss reportó **65**; los 55 restantes quedaron por debajo de su umbral y se registran como similitud 0. El desglose es en sí mismo un resultado: identico 30/30, estructural 27/30, funcional **8/30**, diferente 0/30.

**Similitud media por categoría** (entre los pares reportados): identico 95.0 (rango 79–99), funcional 18.2 (rango 6–44), estructural 65.1 (rango 20–98), diferente sin reportes.

**Resultados con las decisiones declaradas** (banda simétrica 0–20 en *diferente*, tolerancia de 5 puntos en *idéntico*): coincidencia **48.3 %**, sensibilidad **31.1 %**, especificidad **100.0 %**. Por categoría: idéntico 73.3 %, funcional **0.0 %**, estructural 20.0 %, diferente 100.0 %. Por lenguaje: C# 51.7 %, Java 45.0 %.

**Advertencia metodológica sobre la calibración.** Moss nunca devuelve 100 % para archivos idénticos byte a byte: sobre los 30 pares idénticos su similitud osciló entre 79 y 99 (mediana 97). Su porcentaje mide cobertura de coincidencia de *tokens*, no una similitud calibrada donde idéntico equivalga a 100. En consecuencia, la coincidencia agregada depende críticamente de la tolerancia elegida para esa categoría:

| Tolerancia | Banda idéntico | Aciertos en idéntico | Coincidencia global |
|---|---|---|---|
| 0 | 100–100 | 0.0 % | 30.0 % |
| 5 | 95–100 | 73.3 % | 48.3 % |
| 10 | 90–100 | 86.7 % | 51.7 % |
| 20 | 80–100 | 96.7 % | 54.2 % |
| 25 | 75–100 | 100.0 % | 55.0 % |

Una variación de 25 puntos en el resultado global gobernada por un parámetro arbitrario. **Por tanto, la métrica de coincidencia agregada no es una base sólida para un ranking frente a los LLM**, y así debe declararse. Lo comparable y robusto es el patrón por categoría y la distribución de similitud, no el porcentaje global.

**Hallazgo sustantivo.** Moss obtiene **0.0 % en la categoría funcional** y ni siquiera reporta 22 de esos 30 pares, mientras alcanza el 100 % en la categoría *diferente*. Esto confirma empíricamente, con datos reales, la premisa que motiva el artículo: el emparejamiento por huellas dactilares no captura la equivalencia semántica entre implementaciones distintas, aunque discrimina sin error los pares no relacionados.

### Ejecución de Dolos y JPlag

- Versión de Dolos: **[COMPLETAR]**
- Versión de JPlag: **[COMPLETAR]**
- Fecha de ejecución: **[COMPLETAR]**
- Equipo: **[COMPLETAR]**
- Salidas archivadas: **[COMPLETAR: rutas de `pairs.csv`, exportaciones de JPlag y `baselines_raw.csv`]**

**Limitación que debe reconocerse.** La similitud que devuelven estas tres herramientas es solapamiento de huellas o cobertura de *tokens*, no un compuesto ponderado de dimensiones funcional, estructural, léxica y estilística. Evaluarlas contra la misma banda compara constructos distintos.

**Nota ética.** Moss es un servicio remoto: la ejecución sube el corpus a un servidor de Stanford. No hay implicación de privacidad porque los 120 pares fueron autorados para el estudio o extraídos del dominio público y ningún código estudiantil está involucrado. Conviene declararlo, en coherencia con la discusión del artículo sobre el enrutamiento de código a terceros.

---

## 7. Higiene de credenciales

Las cuatro claves de API empleadas en el benchmark quedaron expuestas durante el trabajo y **deben rotarse** (DeepSeek, Google AI Studio, OpenAI, Anthropic). El script `moss` contiene un identificador de usuario que autentica las consultas ante Stanford y **no debe versionarse**: está incluido en `.gitignore` junto con `ejecutar_benchmark.ps1` y `baselines_work/`. Se ha solicitado a `moss-request@cs.stanford.edu` la reposición del identificador.

---

## 8. Pendientes

1. Completar los campos **[COMPLETAR]** de este documento.
2. Ejecutar Dolos y JPlag con el protocolo descrito y archivar sus salidas.
3. Reejecutar la validación Big O contra la API oficial.
4. Evaluación de la calidad de las justificaciones con **dos evaluadores ciegos en escala continua 0–100**, calculando ICC(2,1), para sustituir la escala Likert 1–5 que produjo efecto techo.
5. Decidir el modelo integrado en producción a la luz de los datos nuevos.
6. Regenerar todas las figuras desde los resultados nuevos, con el texto en inglés.
7. Reescribir Resultados, Discusión y Conclusiones con los cuatro modelos actuales.
