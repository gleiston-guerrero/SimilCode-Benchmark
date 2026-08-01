# Registro de ejecuciÃ³n y decisiones â€” SimilCode

Documento de trabajo. Recoge todo lo ejecutado y decidido, con la trazabilidad que necesitan la secciÃ³n de MÃ©todos y la declaraciÃ³n de reproducibilidad. Los campos marcados **[COMPLETAR]** deben rellenarse antes de redactar el manuscrito final.

---

## 1. Benchmark de LLM

**Corpus.** 120 pares controlados, 60 en C# y 60 en Java, balanceados en cuatro categorÃ­as de similitud (30 pares por categorÃ­a). Definido en `metadata.csv` del repositorio SimilCode-Benchmark.

**Modelos evaluados** (identificadores exactos registrados en la columna `model_snapshot` de cada respuesta):

| Proveedor | Identificador invocado |
|---|---|
| DeepSeek | `deepseek-v4-pro` |
| Google | `gemini-3.1-pro-preview` |
| OpenAI | `gpt-5.5-2026-04-23` |
| Anthropic | `claude-opus-5` |

**DiseÃ±o.** Tres rÃ©plicas independientes por par y modelo: 120 Ã— 4 Ã— 3 = **1440 evaluaciones**, todas completadas. El acierto de cada par se determina por voto mayoritario de las tres rÃ©plicas.

**Temperatura.** Se solicitÃ³ 0 en los cuatro proveedores. `claude-opus-5` rechaza ese valor (HTTP 400) por tratarse de un modelo de razonamiento, de modo que sus llamadas se ejecutaron con la temperatura por defecto del proveedor. **Esto debe declararse explÃ­citamente en MÃ©todos.**

**Fechas de recolecciÃ³n.** Del 31 de julio al 1 de agosto de 2026.

**Entornos de ejecuciÃ³n.** La corrida se repartiÃ³ entre dos equipos, por lo que las latencias absolutas mezclan dos configuraciones. El diseÃ±o pareado protege la comparaciÃ³n entre modelos, porque dentro de cada caso los cuatro se ejecutan consecutivamente en la misma mÃ¡quina; aun asÃ­ ambos entornos deben describirse.

- Equipo 1: **[COMPLETAR: CPU, RAM, sistema operativo, ancho de banda]** â€” casos 1 a ~75.
- Equipo 2: **[COMPLETAR: CPU, RAM, sistema operativo, ancho de banda]** â€” casos restantes.

**Incidencias.** El archivo de resultados contiene 182 filas de reintento ademÃ¡s de las 1440 evaluaciones vÃ¡lidas. Se registraron 128 errores HTTP 429 en `gemini-3.1-pro-preview` (lÃ­mite de cuota del modelo *preview*), resueltos mediante reintentos con espera creciente; 30 errores HTTP 400 en Anthropic por el rechazo de `temperature=0`, resueltos reintentando sin ese parÃ¡metro; y 15 errores HTTP 401 en OpenAI por una credencial mal configurada al inicio.

**Prompt.** El archivo `prompt.txt` empleado es una reconstrucciÃ³n fiel del ApÃ©ndice A. **[COMPLETAR: verificar si coincide con el `PROMPT_HASH.txt` original; si no, recalcular el hash SHA-256 del prompt realmente usado y archivarlo.]**

**Datos.** `resultados_replicas.csv` (1622 filas: 1440 evaluaciones vÃ¡lidas + 182 reintentos), archivado en el repositorio.

---

## 2. ValidaciÃ³n de la verdad de terreno

Las 120 parejas fueron clasificadas de forma independiente por dos evaluadores: el investigador principal y un segundo docente de programaciÃ³n ajeno a la construcciÃ³n del conjunto y ciego a las etiquetas originales.

**Acuerdo interevaluador: Îº de Cohen = 0.989** (acuerdo observado 99.2 %, 119 de 120 pares).

El Ãºnico desacuerdo revelÃ³ que la variante funcional del grupo CS_010 se habÃ­a archivado como copia exacta del fragmento idÃ©ntico. Se corrigiÃ³ reemplazando `csharp/CODE_FUN_CS_010.cs` por una reimplementaciÃ³n funcionalmente equivalente (mismo comportamiento y misma salida, implementaciÃ³n distinta). La correcciÃ³n se aplicÃ³ **antes** de que la corrida alcanzara ese caso.

Instrumentos archivados: `categorias_evaluador2.csv` (hoja ciega) y `clave_categorias_ref.csv` (clave, no entregada al evaluador).

---

## 3. Fiabilidad del instrumento de validaciÃ³n con expertos

Calculada sobre `responses/responses_anonymised_wide.csv` del repositorio SimilCode-Validation (5 evaluadores Ã— 18 Ã­tems).

| Subescala | Ãtems | Î± de Cronbach |
|---|---|---|
| Utilidad prÃ¡ctica | Q01â€“Q07 | 1.000 (degenerado) |
| Exactitud de resultados | Q08â€“Q13 | 0.933 |
| Comprensibilidad | Q14â€“Q18 | 0.900 |
| Conjunto de 18 Ã­tems | 18 | 0.661 |

**PatrÃ³n de respuesta detectado.** Los cinco evaluadores respondieron un valor constante a lo largo de los siete Ã­tems de la subescala de utilidad, lo que explica el Î± de 1.000 como artefacto y no como fiabilidad. Tres de los cinco hicieron lo mismo dentro de cada una de las otras dos subescalas. Los Ã­tems Q09 y Q17 no registraron varianza alguna entre participantes.

**CorrecciÃ³n de cifras.** Recalculando desde los datos archivados (promediando primero por evaluador y despuÃ©s entre evaluadores), la subescala de comprensibilidad da **4.60** (el manuscrito indicaba 4.50) y el agregado de los 18 Ã­tems da **4.68 con SD 0.22** (el manuscrito indicaba 4.60 y SD 0.18). Prevalecen los valores derivados de los datos.

---

## 4. ValidaciÃ³n del componente Big O

**Corpus.** 40 algoritmos canÃ³nicos (20 Java, 20 C#) balanceados en siete clases de complejidad temporal de peor caso, mÃ¡s 8 casos adversariales diseÃ±ados para descartar el mero reconocimiento de patrones memorizados (nombres engaÃ±osos, anidamiento con cota constante, bucles secuenciales, memoizaciÃ³n, cÃ³digo muerto de orden superior).

**Resultado.** 48 de 48 correctos en complejidad temporal y espacial (100 %), con matriz de confusiÃ³n estrictamente diagonal.

**ConvenciÃ³n declarada.** Complejidad temporal de **peor caso**; para el espacio, **espacio auxiliar** (excluye la estructura de entrada, incluye la pila de recursiÃ³n).

**CorrecciÃ³n de la verdad de terreno.** La primera puntuaciÃ³n arrojÃ³ tres discrepancias de espacio; el examen mostrÃ³ que en los tres casos el error estaba en la verdad de terreno y no en el modelo. Se corrigiÃ³ `HeapExtractAll` (reserva un arreglo de salida, luego O(n)) y se declarÃ³ la convenciÃ³n de espacio auxiliar. La versiÃ³n previa se conserva como `ground_truth_v1_original.csv`.

**ReejecuciÃ³n contra la API oficial.** El 48/48 inicial se obtuvo con instancias ciegas de `claude-opus-5` dentro de una sesiÃ³n asistida. Se reejecuta con `validar_bigo.py` contra la API oficial, con **k = 3 rÃ©plicas por algoritmo**, para poder informar ademÃ¡s de la consistencia entre rÃ©plicas. **[COMPLETAR: fecha y hora de la corrida definitiva, exactitud por respuesta individual, exactitud por voto mayoritario y porcentaje de algoritmos con las tres rÃ©plicas coincidentes, en los conjuntos canÃ³nico y adversarial.]**

**Criterio de puntuaciÃ³n declarado.** El resultado principal es la **exactitud por respuesta individual**, que penaliza cualquier rÃ©plica errÃ³nea; el voto mayoritario se reporta como dato complementario. El criterio se fijÃ³ antes de ver los resultados.

**Trazabilidad del modelo: limitaciÃ³n declarada.** En la fecha de ejecuciÃ³n, el catÃ¡logo de la API no expone identificador con versiÃ³n fijada para los modelos de la generaciÃ³n actual: `claude-opus-5` figura Ãºnicamente como alias, y solo las generaciones anteriores ofrecen identificadores fechados (`claude-opus-4-5-20251101`, `claude-haiku-4-5-20251001`, `claude-sonnet-4-5-20250929`). La respuesta de la API devuelve el propio alias en el campo `model`, de modo que no hay `model_snapshot` fechado que registrar. Se opta por declarar el **alias junto con la fecha y hora exactas de cada llamada**, que `validar_bigo.py` almacena en la columna `timestamp_utc` de las predicciones. Debe reconocerse en MÃ©todos que un alias puede apuntar a pesos distintos en momentos distintos, y que por tanto la reproducibilidad exacta de esta validaciÃ³n no estÃ¡ garantizada por el proveedor. Es una limitaciÃ³n del ecosistema de modelos propietarios, no del diseÃ±o, y afecta por igual a cualquier estudio que los emplee.

---

## 5. Hallazgo principal: validez de constructo de la mÃ©trica

Los cuatro modelos aplican la fÃ³rmula de ponderaciÃ³n prescrita (Funcional 40 %, Estructural 30 %, LÃ©xica 20 %, EstilÃ­stica 10 %) con fidelidad completa: en el **100 % de las 1435 respuestas** con las cinco dimensiones presentes, el puntaje global reportado coincide con el calculado dentro de Â±5 puntos (diferencia media +0.17).

Sin embargo, la banda esperada y la fÃ³rmula interactÃºan con el criterio de superficie de cada modelo. Calculando quÃ© valor deberÃ­a tener la dimensiÃ³n funcional para caer dentro de la banda, dadas las demÃ¡s dimensiones que el propio modelo asignÃ³:

| Modelo | Funcional requerida (categorÃ­a funcional) | Observada | Alcanzable |
|---|---|---|---|
| GPT-5.5 | â‰¥ 86.1 | 94.3 | SÃ­ |
| DeepSeek-V4-pro | â‰¥ 89.8 | 97.7 | SÃ­ |
| Claude Opus 5 | â‰¥ 104.5 | 90.7 | **No (supera el mÃ¡ximo de 100)** |
| Gemini 3.1 Pro | â‰¥ 115.7 | 98.3 | **No (supera el mÃ¡ximo de 100)** |

Gemini y Claude juzgan la similitud superficial de las reimplementaciones con mÃ¡s severidad (Gemini asigna 30.4 de similitud estructural frente a 57.3 de DeepSeek), lectura igualmente defendible que sin embargo les impide alcanzar la banda.

**Consecuencia.** La mÃ©trica de coincidencia agregada penaliza a los modelos que evalÃºan la superficie con mayor rigor, de modo que el ranking de precisiÃ³n refleja en parte un artefacto de la operacionalizaciÃ³n y no solo capacidad de detecciÃ³n. La raÃ­z es que el tÃ©rmino Â«similitud funcionalÂ» no se define en el prompt: puede leerse como *propÃ³sito de negocio* (Gemini: estudiantes â‰  empleados â†’ 30) o como *patrÃ³n computacional* (los demÃ¡s: listar y clasificar â†’ 65â€“71).

---

## 6. ComparaciÃ³n con detectores clÃ¡sicos

**Advertencia de integridad.** Las cifras de Dolos y JPlag que figuraban en versiones previas del manuscrito (53.3 % y 50.8 %, con sus sensibilidades, especificidades y tiempos) **no proceden de ninguna ejecuciÃ³n** y no deben reutilizarse bajo ninguna forma. El repositorio no contiene datos de esas herramientas.

**Protocolo adoptado.** EjecuciÃ³n en dos modos, reportados por separado: **cohorte** (todas las entregas del lenguaje en una sola corrida, que es el uso real de estas herramientas) y **aislado** (par a par, como suele hacerse en la literatura). La diferencia entre ambos es un resultado reportable.

**Decisiones fijadas a priori:**

- Banda de la categorÃ­a *diferente*: **simÃ©trica** (0â€“20 %, la misma aplicada a los LLM) como resultado principal, y relajada (0â€“30 %) reportada por transparencia.
- Tolerancia en la categorÃ­a *idÃ©ntico*: **5 puntos** a la baja, porque su rango es un punto exacto (100â€“100) y las herramientas de huellas pueden devolver 97â€“99 para archivos idÃ©nticos. Se aplica por igual a todas las herramientas.
- MÃ©trica primaria: `similarity` en Dolos; similitud media en JPlag; media de los dos porcentajes por par en Moss.
- Sin archivo base (`-b`) en ninguna herramienta, en coherencia con el hecho de que SimilCode tampoco excluye plantilla.
- Los pares que Moss no reporta (por debajo de su umbral) se registran como similitud 0.

**MaterializaciÃ³n de los pares idÃ©nticos.** Como ninguna herramienta compara una entrega consigo misma, se genera una copia con sufijo `_COPY` para que la comparaciÃ³n exista realmente.

### EjecuciÃ³n de Moss â€” COMPLETADA

- Servidor: `moss.stanford.edu`, puerto 7690. Cliente Perl oficial ejecutado desde **Git Bash** sobre Windows.
- ParÃ¡metros registrados por el propio servidor: `-l csharp -d -m 10` y `-l java -d -m 10` (una entrega por directorio, sin archivo base).
- Fecha de ejecuciÃ³n: **1 de agosto de 2026, 04:03 PDT**.
- URLs de resultados (caducan; el HTML descargado queda archivado):
  - C#: `http://moss.stanford.edu/results/7/170698045726/` â†’ `moss_cs.html` (43 090 bytes, 143 comparaciones).
  - Java: `http://moss.stanford.edu/results/9/6676565055708/` â†’ `moss_java.html` (68 412 bytes, 228 comparaciones).

**Cobertura.** De los 120 pares del estudio, Moss reportÃ³ **65**; los 55 restantes quedaron por debajo de su umbral y se registran como similitud 0. El desglose es en sÃ­ mismo un resultado: identico 30/30, estructural 27/30, funcional **8/30**, diferente 0/30.

**Similitud media por categorÃ­a** (entre los pares reportados): identico 95.0 (rango 79â€“99), funcional 18.2 (rango 6â€“44), estructural 65.1 (rango 20â€“98), diferente sin reportes.

**Resultados con las decisiones declaradas** (banda simÃ©trica 0â€“20 en *diferente*, tolerancia de 5 puntos en *idÃ©ntico*): coincidencia **48.3 %**, sensibilidad **31.1 %**, especificidad **100.0 %**. Por categorÃ­a: idÃ©ntico 73.3 %, funcional **0.0 %**, estructural 20.0 %, diferente 100.0 %. Por lenguaje: C# 51.7 %, Java 45.0 %.

**Advertencia metodolÃ³gica sobre la calibraciÃ³n.** Moss nunca devuelve 100 % para archivos idÃ©nticos byte a byte: sobre los 30 pares idÃ©nticos su similitud oscilÃ³ entre 79 y 99 (mediana 97). Su porcentaje mide cobertura de coincidencia de *tokens*, no una similitud calibrada donde idÃ©ntico equivalga a 100. En consecuencia, la coincidencia agregada depende crÃ­ticamente de la tolerancia elegida para esa categorÃ­a:

| Tolerancia | Banda idÃ©ntico | Aciertos en idÃ©ntico | Coincidencia global |
|---|---|---|---|
| 0 | 100â€“100 | 0.0 % | 30.0 % |
| 5 | 95â€“100 | 73.3 % | 48.3 % |
| 10 | 90â€“100 | 86.7 % | 51.7 % |
| 20 | 80â€“100 | 96.7 % | 54.2 % |
| 25 | 75â€“100 | 100.0 % | 55.0 % |

Una variaciÃ³n de 25 puntos en el resultado global gobernada por un parÃ¡metro arbitrario. **Por tanto, la mÃ©trica de coincidencia agregada no es una base sÃ³lida para un ranking frente a los LLM**, y asÃ­ debe declararse. Lo comparable y robusto es el patrÃ³n por categorÃ­a y la distribuciÃ³n de similitud, no el porcentaje global.

**Hallazgo sustantivo.** Moss obtiene **0.0 % en la categorÃ­a funcional** y ni siquiera reporta 22 de esos 30 pares, mientras alcanza el 100 % en la categorÃ­a *diferente*. Esto confirma empÃ­ricamente, con datos reales, la premisa que motiva el artÃ­culo: el emparejamiento por huellas dactilares no captura la equivalencia semÃ¡ntica entre implementaciones distintas, aunque discrimina sin error los pares no relacionados.

### EjecuciÃ³n de JPlag â€” COMPLETADA

- VersiÃ³n de JPlag: **[COMPLETAR: salida de `java -jar jplag.jar --version`]**
- Fecha de ejecuciÃ³n: **1 de agosto de 2026, 13:46 (hora local del equipo)**.
- Equipo: **[COMPLETAR: CPU, RAM, sistema operativo]**
- ParÃ¡metros: `-l csharp` y `-l java`, `--csv-export`, `-n -1` (sin truncar el informe), `--overwrite`. Umbral de similitud en su valor por defecto **0.0**, de modo que JPlag emite un valor para las 2 775 comparaciones de cada lenguaje y ningÃºn par queda sin reportar.
- Salidas archivadas: `out_jplag_cs/results.csv` y `out_jplag_java/results.csv` (2 775 comparaciones cada uno), mÃ¡s los contenedores `out_jplag_cs.jplag` y `out_jplag_java.jplag`. Logs completos en `jplag_cs.log` y `jplag_java.log`.

**DecisiÃ³n declarada sobre la mÃ©trica.** JPlag emite dos magnitudes por par, `averageSimilarity` y `maxSimilarity`. Se toma **siempre `averageSimilarity`**, por ser la magnitud simÃ©trica comparable con la `similarity` de Dolos y con la media de los dos porcentajes direccionales de Moss. Emplear `maxSimilarity` producirÃ­a cifras sistemÃ¡ticamente mÃ¡s altas y una comparaciÃ³n desigual entre herramientas.

**Cobertura sintÃ¡ctica: fallos de anÃ¡lisis en C#.** La gramÃ¡tica de C# de JPlag no cubre construcciones habituales del lenguaje contemporÃ¡neo y emitiÃ³ 87 errores de anÃ¡lisis sobre **13 de las 75 entregas de C# (17,3 %)**. Las causas identificadas son: expresiones `new()` con tipo inferido, `async`/`await`/`Task`, literales `decimal` con sufijo `m`, propiedades autoimplementadas con inicializador, genÃ©ricos anidados y cadenas interpoladas con especificador de formato. Cuando el anÃ¡lisis falla, JPlag no se detiene: tokeniza de forma incompleta y continÃºa, por lo que la similitud de esas entregas no es plenamente fiable.

El efecto sobre el diseÃ±o es acotado y se distribuye asÃ­: **13 de los 120 pares (10,8 %)** contienen al menos una entrega afectada â€” idÃ©ntico 0/30, funcional 6/30, estructural 1/30, diferente 6/30. Que la categorÃ­a *idÃ©ntico* quede intacta es relevante porque preserva el ancla de calibraciÃ³n. La cohorte de **Java se analizÃ³ sin un solo error**, lo que convierte el contraste en un resultado por derecho propio sobre la cobertura sintÃ¡ctica desigual de una herramienta clÃ¡sica segÃºn el lenguaje. CuantificaciÃ³n reproducible mediante `baselines.py antlr`, con salida archivada en `antlr_cs.csv`.

**Resultados con las decisiones declaradas** (banda simÃ©trica, tolerancia de 5 puntos en *idÃ©ntico*): coincidencia **50,0 %**, sensibilidad **34,4 %**, especificidad **96,7 %**. Por categorÃ­a: idÃ©ntico **100,0 %**, funcional **0,0 %**, estructural **3,3 %**, diferente **96,7 %**. Similitud media por categorÃ­a: idÃ©ntico 100,0, funcional 10,5, estructural 85,6, diferente 1,9.

**CalibraciÃ³n.** A diferencia de Moss, JPlag sÃ­ devuelve exactamente 100 para los 30 pares byte a byte idÃ©nticos, de modo que su resultado en esa categorÃ­a no depende de la tolerancia elegida. Esta diferencia de comportamiento entre dos herramientas del mismo gÃ©nero refuerza la conclusiÃ³n de que la coincidencia agregada no es una base sÃ³lida para un ranking.

**Hallazgo sustantivo: insensibilidad al renombrado.** JPlag normaliza los identificadores antes de comparar, por lo que una variante que conserva el flujo de control y solo cambia nombres le resulta indistinguible del original. El caso `CODE_ESTRU_CS_010` frente a `CODE_IDENT_CS_010` recibe similitud 1,0 pese a que los dos archivos difieren (SHA-256 `420392EEâ€¦` y `B04E4828â€¦`). No es un caso aislado: de los 30 pares estructurales, **16 reciben exactamente 100** y **19 quedan en 90 o mÃ¡s**, con una media de **85,6** frente a una banda esperada muy inferior; solo el 3,3 % cae dentro de ella. Es decir, en mÃ¡s de la mitad de los pares estructurales JPlag no distingue una variante reescrita de una copia literal. Moss, que no normaliza identificadores del mismo modo, promedia 58,6 en esa misma categorÃ­a.

**Convergencia entre Moss y JPlag.** Ambas herramientas obtienen **0,0 % en la categorÃ­a funcional** â€” media de similitud 4,9 en Moss y 10,5 en JPlag â€” mientras discriminan casi sin error los pares no relacionados. Dos implementaciones independientes de familias algorÃ­tmicas distintas (huellas por *winnowing* frente a comparaciÃ³n de cadenas de *tokens*) coinciden en el mismo punto ciego, lo que fortalece la premisa del artÃ­culo: el emparejamiento sintÃ¡ctico no captura la equivalencia semÃ¡ntica entre implementaciones distintas.

**Cautela sobre la especificidad.** Las cifras altas en la categorÃ­a *diferente* (96,7 % y 100 %) deben leerse con reserva: un detector degenerado que devolviera 0 para todo par obtendrÃ­a el 100 % en esa categorÃ­a y el 0 % en las demÃ¡s, con una coincidencia agregada del 25 %. La especificidad es aquÃ­ casi gratuita, y no debe presentarse como una fortaleza comparativa. Lo informativo es el perfil completo: ambas herramientas aciertan en *idÃ©ntico*, sobrestiman en *estructural* y son ciegas en *funcional*.

### EjecuciÃ³n de Dolos â€” COMPLETADA

- VersiÃ³n: **Dolos v2.9.3**, sobre Node v22.23.2 y Tree-sitter ^0.25.0.
- Entorno: **WSL 2.7.11 con Ubuntu**, sobre el mismo equipo Windows. Dolos compila analizadores nativos con `node-gyp` y no pudo instalarse en Windows por ausencia de las herramientas de C++ de Visual Studio; la instalaciÃ³n en Linux es la vÃ­a practicable y debe declararse como parte del entorno de ejecuciÃ³n.
- Claves de lenguaje aceptadas por `-l`: **`c-sharp`** y **`java`**. La clave `csharp` es rechazada (Dolos construye el nombre del paquete como `tree-sitter-<clave>`). Este dato no estÃ¡ documentado y se determinÃ³ empÃ­ricamente.
- Fecha de ejecuciÃ³n: **1 de agosto de 2026**.
- ParÃ¡metros: `-f csv`, `-S 0` (sin filtrar pares por similitud mÃ­nima, de modo que emite valor para las 2 775 comparaciones de cada lenguaje), `--no-open`. Valores por defecto en `-k 23` (longitud de k-grama), `-w 17` (ventana), `-M 0.9` (descarte de huellas presentes en mÃ¡s del 90 % de los archivos) y exclusiÃ³n de comentarios. No se suministrÃ³ archivo de plantilla (`-i`), en coherencia con Moss y JPlag.
- Salidas archivadas: `out_dolos_cs/` y `out_dolos_java/` (principal), `out_dolos_cs_m10/` y `out_dolos_java_m10/` (sensibilidad). Cada carpeta contiene `pairs.csv`, `files.csv`, `kgrams.csv` y `metadata.csv`.

**AnÃ¡lisis de sensibilidad al descuento de plantilla.** Moss emplea `-m 10` (descarta la huella presente en mÃ¡s de diez programas) y Dolos, por defecto, `-M 0.9` (mÃ¡s del 90 % de los archivos). Sobre 75 entregas no son protocolos equivalentes: el de Moss es mucho mÃ¡s estricto. Se ejecutÃ³ por ello una segunda corrida de Dolos con `-m 10` para armonizar el criterio. El resultado desaconseja esa armonizaciÃ³n: la coincidencia de Dolos cae de 44,2 % a 36,7 %, y sobre todo su acierto en la categorÃ­a *idÃ©ntico* se desploma del **100 % al 16,7 %**, porque el filtro elimina las huellas compartidas por los pares byte a byte. Se concluye que el parÃ¡metro no es transferible entre herramientas y que **cada una debe evaluarse con sus valores por defecto**, que son los de su uso institucional real. La corrida armonizada se conserva como anÃ¡lisis de sensibilidad declarado, no como resultado principal.

**Advertencia de procesamiento (relevante para la reproducibilidad).** Dolos identifica las entregas por **archivo**, mientras que Moss (`-d`) y JPlag lo hacen por **carpeta**. En el diseÃ±o de `preparar`, la copia materializada de cada par idÃ©ntico vive en una carpeta `X_COPY` pero el archivo interior conserva el nombre `X.<ext>`. Tomar el nombre del archivo hace colapsar cada copia con su original: las 2 775 comparaciones se funden en 1 785 claves distintas â€”exactamente C(60,2)+15â€” y **todas** las cifras de Dolos quedan contaminadas, no solo las de la categorÃ­a idÃ©ntico. El parser resuelve el nombre de entrega desde la carpeta contenedora, y `parsear` verifica ahora que el nÃºmero de filas leÃ­das coincida con el de pares distintos. Cualquier reejecuciÃ³n debe comprobar que Dolos lee 2 775 filas â†’ 2 775 pares distintos y 75 entregas.

**Resultados con las decisiones declaradas** (banda simÃ©trica, tolerancia de 5 puntos en *idÃ©ntico*): coincidencia **44,2 %**, sensibilidad **36,7 %**, especificidad **66,7 %**. Por categorÃ­a: idÃ©ntico **100,0 %**, funcional **0,0 %**, estructural **10,0 %**, diferente **66,7 %**. Similitud media por categorÃ­a: idÃ©ntico 100,0, funcional 27,8, estructural 77,4, diferente 13,6.

### SÃ­ntesis de las tres herramientas clÃ¡sicas

| | Moss | JPlag | Dolos |
|---|---|---|---|
| Familia algorÃ­tmica | huellas por *winnowing* | cadenas de *tokens* | *tree-sitter* sobre AST |
| Coincidencia global | 48,3 % | 50,0 % | 44,2 % |
| Sensibilidad | 31,1 % | 34,4 % | 36,7 % |
| Especificidad | 100,0 % | 96,7 % | 66,7 % |
| IdÃ©ntico | 73,3 % | 100,0 % | 100,0 % |
| **Funcional** | **0,0 %** | **0,0 %** | **0,0 %** |
| Estructural | 20,0 % | 3,3 % | 10,0 % |
| Diferente | 100,0 % | 96,7 % | 66,7 % |
| Media en *funcional* | 4,9 | 10,5 | 27,8 |
| Media en *estructural* | 58,6 | 85,6 | 77,4 |

**Hallazgo principal de la comparaciÃ³n.** Tres herramientas de tres familias algorÃ­tmicas distintas obtienen **0,0 % en la categorÃ­a funcional**, con similitudes medias de 4,9, 10,5 y 27,8 sobre pares que resuelven el mismo problema con implementaciones diferentes. La unanimidad es lo que convierte el resultado en evidencia: no es una limitaciÃ³n de una implementaciÃ³n concreta, sino del constructo que las tres miden. Dolos, la mÃ¡s moderna y la Ãºnica que trabaja sobre el Ã¡rbol sintÃ¡ctico, es tambiÃ©n la que mÃ¡s se acerca â€”media 27,8 frente a 4,9 de Mossâ€”, lo que sugiere que el anÃ¡lisis estructural profundo reduce la brecha pero no la cierra.

**Segundo hallazgo: sobrestimaciÃ³n en la categorÃ­a estructural.** Las tres sitÃºan la similitud estructural por encima de lo esperado, y el orden reproduce su grado de abstracciÃ³n sintÃ¡ctica: Moss 58,6, Dolos 77,4, JPlag 85,6. En JPlag el efecto es extremo â€”16 de 30 pares estructurales reciben exactamente 100â€” porque normaliza los identificadores y una variante que solo cambia nombres le resulta idÃ©ntica al original.

**Cautelas que deben acompaÃ±ar a esta tabla.**

La coincidencia global apenas separa a las tres herramientas (44,2â€“50,0 %) y tampoco las separa mucho de los LLM (~60 %). Un *ranking* construido sobre esa cifra serÃ­a frÃ¡gil. Lo que separa de verdad es el perfil por categorÃ­a, donde la diferencia es cualitativa.

Las cifras altas en la categorÃ­a *diferente* deben leerse con reserva: un detector degenerado que devolviera 0 para todo par obtendrÃ­a el 100 % en esa categorÃ­a, el 0 % en las demÃ¡s y una coincidencia global del 25 %. La especificidad es aquÃ­ casi gratuita y no debe presentarse como fortaleza comparativa. Que Dolos baje al 66,7 % refleja que asigna similitud no trivial (media 13,6) a pares no relacionados.

Los 55 pares que Moss no reporta se registran como cero por decisiÃ³n nuestra (`--faltantes-cero`), lo que empuja su especificidad al 100 %. JPlag y Dolos no necesitan esa convenciÃ³n porque emiten valor para todas las comparaciones. Esta asimetrÃ­a entre herramientas debe declararse.

**LimitaciÃ³n que debe reconocerse.** La similitud que devuelven estas tres herramientas es solapamiento de huellas o cobertura de *tokens*, no un compuesto ponderado de dimensiones funcional, estructural, lÃ©xica y estilÃ­stica. Evaluarlas contra la misma banda compara constructos distintos, y asÃ­ debe presentarse: como evidencia sobre quÃ© captura cada enfoque, no como una competiciÃ³n con un ganador.

**Nota Ã©tica.** Moss es un servicio remoto: la ejecuciÃ³n sube el corpus a un servidor de Stanford. No hay implicaciÃ³n de privacidad porque los 120 pares fueron autorados para el estudio o extraÃ­dos del dominio pÃºblico y ningÃºn cÃ³digo estudiantil estÃ¡ involucrado. Conviene declararlo, en coherencia con la discusiÃ³n del artÃ­culo sobre el enrutamiento de cÃ³digo a terceros.

---

## 7. Higiene de credenciales

Las cuatro claves de API empleadas en el benchmark quedaron expuestas durante el trabajo y **deben rotarse** (DeepSeek, Google AI Studio, OpenAI, Anthropic). El script `moss` contiene un identificador de usuario que autentica las consultas ante Stanford y **no debe versionarse**: estÃ¡ incluido en `.gitignore` junto con `ejecutar_benchmark.ps1` y `baselines_work/`. Se ha solicitado a `moss-request@cs.stanford.edu` la reposiciÃ³n del identificador.

---

## 8. Pendientes

1. Completar los campos **[COMPLETAR]** de este documento.
2. Sustituir en las secciones 3.6 y 4.5 del manuscrito las cifras inventadas de lÃ­neas base por los resultados reales de Moss, JPlag y Dolos recogidos arriba.
3. Reejecutar la validaciÃ³n Big O contra la API oficial.
4. EvaluaciÃ³n de la calidad de las justificaciones con **dos evaluadores ciegos en escala continua 0â€“100**, calculando ICC(2,1), para sustituir la escala Likert 1â€“5 que produjo efecto techo.
5. Decidir el modelo integrado en producciÃ³n a la luz de los datos nuevos.
6. Regenerar todas las figuras desde los resultados nuevos, con el texto en inglÃ©s.
7. Reescribir Resultados, DiscusiÃ³n y Conclusiones con los cuatro modelos actuales.
