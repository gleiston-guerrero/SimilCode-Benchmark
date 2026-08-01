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

**Reejecución contra la API oficial.** El 48/48 inicial se obtuvo con instancias ciegas de `claude-opus-5` dentro de una sesión asistida. Se reejecuta con `validar_bigo.py` contra la API oficial, con **k = 3 réplicas por algoritmo**, para poder informar además de la consistencia entre réplicas. **[COMPLETAR: fecha y hora de la corrida definitiva, exactitud por respuesta individual, exactitud por voto mayoritario y porcentaje de algoritmos con las tres réplicas coincidentes, en los conjuntos canónico y adversarial.]**

**Criterio de puntuación declarado.** El resultado principal es la **exactitud por respuesta individual**, que penaliza cualquier réplica errónea; el voto mayoritario se reporta como dato complementario. El criterio se fijó antes de ver los resultados.

**Trazabilidad del modelo: limitación declarada.** En la fecha de ejecución, el catálogo de la API no expone identificador con versión fijada para los modelos de la generación actual: `claude-opus-5` figura únicamente como alias, y solo las generaciones anteriores ofrecen identificadores fechados (`claude-opus-4-5-20251101`, `claude-haiku-4-5-20251001`, `claude-sonnet-4-5-20250929`). La respuesta de la API devuelve el propio alias en el campo `model`, de modo que no hay `model_snapshot` fechado que registrar. Se opta por declarar el **alias junto con la fecha y hora exactas de cada llamada**, que `validar_bigo.py` almacena en la columna `timestamp_utc` de las predicciones. Debe reconocerse en Métodos que un alias puede apuntar a pesos distintos en momentos distintos, y que por tanto la reproducibilidad exacta de esta validación no está garantizada por el proveedor. Es una limitación del ecosistema de modelos propietarios, no del diseño, y afecta por igual a cualquier estudio que los emplee.

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

- Servidor: `moss.stanford.edu`, puerto 7690. Cliente Perl oficial ejecutado desde **Git Bash** sobre Windows.
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

### Ejecución de JPlag — COMPLETADA

- Versión de JPlag: **[COMPLETAR: salida de `java -jar jplag.jar --version`]**
- Fecha de ejecución: **1 de agosto de 2026, 13:46 (hora local del equipo)**.
- Equipo: **[COMPLETAR: CPU, RAM, sistema operativo]**
- Parámetros: `-l csharp` y `-l java`, `--csv-export`, `-n -1` (sin truncar el informe), `--overwrite`. Umbral de similitud en su valor por defecto **0.0**, de modo que JPlag emite un valor para las 2 775 comparaciones de cada lenguaje y ningún par queda sin reportar.
- Salidas archivadas: `out_jplag_cs2/results.csv` y `out_jplag_java/results.csv` (2 775 comparaciones cada uno), más los contenedores `out_jplag_cs2.jplag` y `out_jplag_java.jplag`. Logs completos en `jplag_cs.log` y `jplag_java.log`.

**Decisión declarada sobre la métrica.** JPlag emite dos magnitudes por par, `averageSimilarity` y `maxSimilarity`. Se toma **siempre `averageSimilarity`**, por ser la magnitud simétrica comparable con la `similarity` de Dolos y con la media de los dos porcentajes direccionales de Moss. Emplear `maxSimilarity` produciría cifras sistemáticamente más altas y una comparación desigual entre herramientas.

**Cobertura sintáctica: fallos de análisis en C#.** La gramática de C# de JPlag no cubre construcciones habituales del lenguaje contemporáneo y emitió 87 errores de análisis sobre **13 de las 75 entregas de C# (17,3 %)**. Las causas identificadas son: expresiones `new()` con tipo inferido, `async`/`await`/`Task`, literales `decimal` con sufijo `m`, propiedades autoimplementadas con inicializador, genéricos anidados y cadenas interpoladas con especificador de formato. Cuando el análisis falla, JPlag no se detiene: tokeniza de forma incompleta y continúa, por lo que la similitud de esas entregas no es plenamente fiable.

El efecto sobre el diseño es acotado y se distribuye así: **13 de los 120 pares (10,8 %)** contienen al menos una entrega afectada — idéntico 0/30, funcional 6/30, estructural 1/30, diferente 6/30. Que la categoría *idéntico* quede intacta es relevante porque preserva el ancla de calibración. La cohorte de **Java se analizó sin un solo error**, lo que convierte el contraste en un resultado por derecho propio sobre la cobertura sintáctica desigual de una herramienta clásica según el lenguaje. Cuantificación reproducible mediante `baselines.py antlr`, con salida archivada en `antlr_cs.csv`.

**Resultados con las decisiones declaradas** (banda simétrica, tolerancia de 5 puntos en *idéntico*): coincidencia **50,0 %**, sensibilidad **34,4 %**, especificidad **96,7 %**. Por categoría: idéntico **100,0 %**, funcional **0,0 %**, estructural **3,3 %**, diferente **96,7 %**. Similitud media por categoría: idéntico 100,0, funcional 10,5, estructural 85,6, diferente 1,9.

**Calibración.** A diferencia de Moss, JPlag sí devuelve exactamente 100 para los 30 pares byte a byte idénticos, de modo que su resultado en esa categoría no depende de la tolerancia elegida. Esta diferencia de comportamiento entre dos herramientas del mismo género refuerza la conclusión de que la coincidencia agregada no es una base sólida para un ranking.

**Hallazgo sustantivo: insensibilidad al renombrado.** JPlag normaliza los identificadores antes de comparar, por lo que una variante que conserva el flujo de control y solo cambia nombres le resulta indistinguible del original. El caso `CODE_ESTRU_CS_010` frente a `CODE_IDENT_CS_010` recibe similitud 1,0 pese a que los dos archivos difieren (SHA-256 `420392EE…` y `B04E4828…`). No es un caso aislado: de los 30 pares estructurales, **16 reciben exactamente 100** y **19 quedan en 90 o más**, con una media de **85,6** frente a una banda esperada muy inferior; solo el 3,3 % cae dentro de ella. Es decir, en más de la mitad de los pares estructurales JPlag no distingue una variante reescrita de una copia literal. Moss, que no normaliza identificadores del mismo modo, promedia 58,6 en esa misma categoría.

**Convergencia entre Moss y JPlag.** Ambas herramientas obtienen **0,0 % en la categoría funcional** — media de similitud 4,9 en Moss y 10,5 en JPlag — mientras discriminan casi sin error los pares no relacionados. Dos implementaciones independientes de familias algorítmicas distintas (huellas por *winnowing* frente a comparación de cadenas de *tokens*) coinciden en el mismo punto ciego, lo que fortalece la premisa del artículo: el emparejamiento sintáctico no captura la equivalencia semántica entre implementaciones distintas.

**Cautela sobre la especificidad.** Las cifras altas en la categoría *diferente* (96,7 % y 100 %) deben leerse con reserva: un detector degenerado que devolviera 0 para todo par obtendría el 100 % en esa categoría y el 0 % en las demás, con una coincidencia agregada del 25 %. La especificidad es aquí casi gratuita, y no debe presentarse como una fortaleza comparativa. Lo informativo es el perfil completo: ambas herramientas aciertan en *idéntico*, sobrestiman en *estructural* y son ciegas en *funcional*.

### Ejecución de Dolos — COMPLETADA

- Versión: **Dolos v2.9.3**, sobre Node v22.23.2 y Tree-sitter ^0.25.0.
- Entorno: **WSL 2.7.11 con Ubuntu**, sobre el mismo equipo Windows. Dolos compila analizadores nativos con `node-gyp` y no pudo instalarse en Windows por ausencia de las herramientas de C++ de Visual Studio; la instalación en Linux es la vía practicable y debe declararse como parte del entorno de ejecución.
- Claves de lenguaje aceptadas por `-l`: **`c-sharp`** y **`java`**. La clave `csharp` es rechazada (Dolos construye el nombre del paquete como `tree-sitter-<clave>`). Este dato no está documentado y se determinó empíricamente.
- Fecha de ejecución: **1 de agosto de 2026**.
- Parámetros: `-f csv`, `-S 0` (sin filtrar pares por similitud mínima, de modo que emite valor para las 2 775 comparaciones de cada lenguaje), `--no-open`. Valores por defecto en `-k 23` (longitud de k-grama), `-w 17` (ventana), `-M 0.9` (descarte de huellas presentes en más del 90 % de los archivos) y exclusión de comentarios. No se suministró archivo de plantilla (`-i`), en coherencia con Moss y JPlag.
- Salidas archivadas: `out_dolos_cs/` y `out_dolos_java/` (principal), `out_dolos_cs_m10/` y `out_dolos_java_m10/` (sensibilidad). Cada carpeta contiene `pairs.csv`, `files.csv`, `kgrams.csv` y `metadata.csv`.

**Análisis de sensibilidad al descuento de plantilla.** Moss emplea `-m 10` (descarta la huella presente en más de diez programas) y Dolos, por defecto, `-M 0.9` (más del 90 % de los archivos). Sobre 75 entregas no son protocolos equivalentes: el de Moss es mucho más estricto. Se ejecutó por ello una segunda corrida de Dolos con `-m 10` para armonizar el criterio. El resultado desaconseja esa armonización: la coincidencia de Dolos cae de 44,2 % a 36,7 %, y sobre todo su acierto en la categoría *idéntico* se desploma del **100 % al 16,7 %**, porque el filtro elimina las huellas compartidas por los pares byte a byte. Se concluye que el parámetro no es transferible entre herramientas y que **cada una debe evaluarse con sus valores por defecto**, que son los de su uso institucional real. La corrida armonizada se conserva como análisis de sensibilidad declarado, no como resultado principal.

**Advertencia de procesamiento (relevante para la reproducibilidad).** Dolos identifica las entregas por **archivo**, mientras que Moss (`-d`) y JPlag lo hacen por **carpeta**. En el diseño de `preparar`, la copia materializada de cada par idéntico vive en una carpeta `X_COPY` pero el archivo interior conserva el nombre `X.<ext>`. Tomar el nombre del archivo hace colapsar cada copia con su original: las 2 775 comparaciones se funden en 1 785 claves distintas —exactamente C(60,2)+15— y **todas** las cifras de Dolos quedan contaminadas, no solo las de la categoría idéntico. El parser resuelve el nombre de entrega desde la carpeta contenedora, y `parsear` verifica ahora que el número de filas leídas coincida con el de pares distintos. Cualquier reejecución debe comprobar que Dolos lee 2 775 filas → 2 775 pares distintos y 75 entregas.

**Resultados con las decisiones declaradas** (banda simétrica, tolerancia de 5 puntos en *idéntico*): coincidencia **44,2 %**, sensibilidad **36,7 %**, especificidad **66,7 %**. Por categoría: idéntico **100,0 %**, funcional **0,0 %**, estructural **10,0 %**, diferente **66,7 %**. Similitud media por categoría: idéntico 100,0, funcional 27,8, estructural 77,4, diferente 13,6.

### Síntesis de las tres herramientas clásicas

| | Moss | JPlag | Dolos |
|---|---|---|---|
| Familia algorítmica | huellas por *winnowing* | cadenas de *tokens* | *tree-sitter* sobre AST |
| Coincidencia global | 48,3 % | 50,0 % | 44,2 % |
| Sensibilidad | 31,1 % | 34,4 % | 36,7 % |
| Especificidad | 100,0 % | 96,7 % | 66,7 % |
| Idéntico | 73,3 % | 100,0 % | 100,0 % |
| **Funcional** | **0,0 %** | **0,0 %** | **0,0 %** |
| Estructural | 20,0 % | 3,3 % | 10,0 % |
| Diferente | 100,0 % | 96,7 % | 66,7 % |
| Media en *funcional* | 4,9 | 10,5 | 27,8 |
| Media en *estructural* | 58,6 | 85,6 | 77,4 |

**Hallazgo principal de la comparación.** Tres herramientas de tres familias algorítmicas distintas obtienen **0,0 % en la categoría funcional**, con similitudes medias de 4,9, 10,5 y 27,8 sobre pares que resuelven el mismo problema con implementaciones diferentes. La unanimidad es lo que convierte el resultado en evidencia: no es una limitación de una implementación concreta, sino del constructo que las tres miden. Dolos, la más moderna y la única que trabaja sobre el árbol sintáctico, es también la que más se acerca —media 27,8 frente a 4,9 de Moss—, lo que sugiere que el análisis estructural profundo reduce la brecha pero no la cierra.

**Segundo hallazgo: sobrestimación en la categoría estructural.** Las tres sitúan la similitud estructural por encima de lo esperado, y el orden reproduce su grado de abstracción sintáctica: Moss 58,6, Dolos 77,4, JPlag 85,6. En JPlag el efecto es extremo —16 de 30 pares estructurales reciben exactamente 100— porque normaliza los identificadores y una variante que solo cambia nombres le resulta idéntica al original.

**Cautelas que deben acompañar a esta tabla.**

La coincidencia global apenas separa a las tres herramientas (44,2–50,0 %) y tampoco las separa mucho de los LLM (~60 %). Un *ranking* construido sobre esa cifra sería frágil. Lo que separa de verdad es el perfil por categoría, donde la diferencia es cualitativa.

Las cifras altas en la categoría *diferente* deben leerse con reserva: un detector degenerado que devolviera 0 para todo par obtendría el 100 % en esa categoría, el 0 % en las demás y una coincidencia global del 25 %. La especificidad es aquí casi gratuita y no debe presentarse como fortaleza comparativa. Que Dolos baje al 66,7 % refleja que asigna similitud no trivial (media 13,6) a pares no relacionados.

Los 55 pares que Moss no reporta se registran como cero por decisión nuestra (`--faltantes-cero`), lo que empuja su especificidad al 100 %. JPlag y Dolos no necesitan esa convención porque emiten valor para todas las comparaciones. Esta asimetría entre herramientas debe declararse.

**Limitación que debe reconocerse.** La similitud que devuelven estas tres herramientas es solapamiento de huellas o cobertura de *tokens*, no un compuesto ponderado de dimensiones funcional, estructural, léxica y estilística. Evaluarlas contra la misma banda compara constructos distintos, y así debe presentarse: como evidencia sobre qué captura cada enfoque, no como una competición con un ganador.

**Nota ética.** Moss es un servicio remoto: la ejecución sube el corpus a un servidor de Stanford. No hay implicación de privacidad porque los 120 pares fueron autorados para el estudio o extraídos del dominio público y ningún código estudiantil está involucrado. Conviene declararlo, en coherencia con la discusión del artículo sobre el enrutamiento de código a terceros.

---

## 7. Higiene de credenciales

Las cuatro claves de API empleadas en el benchmark quedaron expuestas durante el trabajo y **deben rotarse** (DeepSeek, Google AI Studio, OpenAI, Anthropic). El script `moss` contiene un identificador de usuario que autentica las consultas ante Stanford y **no debe versionarse**: está incluido en `.gitignore` junto con `ejecutar_benchmark.ps1` y `baselines_work/`. Se ha solicitado a `moss-request@cs.stanford.edu` la reposición del identificador.

---

## 8. Pendientes

1. Completar los campos **[COMPLETAR]** de este documento.
2. Sustituir en las secciones 3.6 y 4.5 del manuscrito las cifras inventadas de líneas base por los resultados reales de Moss, JPlag y Dolos recogidos arriba.
3. Reejecutar la validación Big O contra la API oficial.
4. Evaluación de la calidad de las justificaciones con **dos evaluadores ciegos en escala continua 0–100**, calculando ICC(2,1), para sustituir la escala Likert 1–5 que produjo efecto techo.
5. Decidir el modelo integrado en producción a la luz de los datos nuevos.
6. Regenerar todas las figuras desde los resultados nuevos, con el texto en inglés.
7. Reescribir Resultados, Discusión y Conclusiones con los cuatro modelos actuales.
