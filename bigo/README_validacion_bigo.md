# Validación del componente de estimación de complejidad algorítmica

Este paquete valida el estimador Big O de SimilCode frente a un conjunto curado de algoritmos con complejidad documentada.

## Qué archivos respaldan el artículo

Esta carpeta contiene, junto a los definitivos, archivos de corridas anteriores que se conservan por trazabilidad. Para evitar confusiones, esta es la correspondencia exacta:

**Resultados que respaldan el manuscrito** — corrida del 3 de agosto de 2026 con el modelo de producción `gpt-5.5-2026-04-23`, tres réplicas independientes por algoritmo:

| Archivo | Contenido |
|---|---|
| `predicciones_api.csv` | 120 respuestas sobre el corpus canónico (40 algoritmos × 3 réplicas) |
| `predicciones_api_adv.csv` | 24 respuestas sobre el conjunto adversarial (8 × 3) |
| `resultados_bigo_api.csv` | Comparación caso a caso contra la verdad de terreno, conjunto canónico |
| `resultados_bigo_adv_api.csv` | Comparación caso a caso, conjunto adversarial |

**Archivos intermedios, conservados por trazabilidad y que NO respaldan el artículo:**

| Archivo | Por qué existe |
|---|---|
| `predicciones_opus5.csv` | Corrida preliminar con otro modelo, anterior a la decisión del modelo de producción |
| `predicciones_adversarial_opus5.csv` | Ídem, sobre el conjunto adversarial |
| `resultados_bigo.csv` | Comparación correspondiente a esa corrida preliminar |
| `ground_truth_v1_original.csv` | Verdad de terreno anterior a la corrección documentada más abajo |

**Advertencia sobre el historial.** El archivo `predicciones_api.csv` existió con contenido distinto en commits anteriores de este repositorio: fue añadido en `7a5330b`, retirado en `f221d76` y repuesto con su contenido definitivo en `132c39c`. Quien reproduzca los resultados debe usar la versión de la rama principal actual. El contenido correcto se reconoce por sus columnas `provider`, `model_requested` y `model_snapshot`, que deben valer `openai` y `gpt-5.5-2026-04-23`, y por su columna `replica`, con valores 1 a 3.

## Diseño

**Corpus canónico (40 algoritmos).** 20 en Java y 20 en C#, balanceados en siete clases de complejidad temporal de peor caso: O(1) — 4 casos; O(log n) — 6; O(n) — 9; O(n log n) — 4; O(n²) — 10; O(n³) — 3; O(2ⁿ) — 4. Incluye búsquedas, ordenamientos, recorridos de grafos sobre matriz de adyacencia, programación dinámica y recursión exponencial.

**Conjunto adversarial (8 casos).** Diseñado para que el corpus discrimine y no se limite a medir el reconocimiento de algoritmos de libro de texto: nombres y comentarios que contradicen la estructura real, anidamiento aparente con cota interna constante, bucles secuenciales que no se multiplican, memoización que colapsa una recursión binaria, código muerto de orden superior y división sucesiva disfrazada de recorrido lineal.

**Verdad de terreno.** Complejidad temporal de peor caso, con las siete clases anteriores. Para el espacio se adopta la convención de **espacio auxiliar** —excluye la estructura de entrada, incluye la pila de recursión—, declarada explícitamente en `ground_truth.csv`. Las fuentes se documentan por entrada; los resultados estándar provienen de Cormen et al. (2022), *Introduction to Algorithms*, 4.ª ed.

**Procedimiento.** Cada fragmento se evalúa de forma independiente con el prompt estandarizado `bigo_prompt.txt`, con tres réplicas por algoritmo. El evaluador es ciego: recibe únicamente el código, nunca la complejidad documentada ni el nombre del archivo de verdad de terreno, que vive en un árbol de directorios separado.

## Resultados

| Conjunto | Respuestas | Exactitud temporal | Exactitud espacial |
|---|---|---|---|
| Canónico | 120 (40 × 3) | 100.0 % | 100.0 % |
| Adversarial | 24 (8 × 3) | 100.0 % | 100.0 % |
| **Total** | **144** | **100.0 %** | **100.0 %** |

La exactitud es del 100 % en cada una de las siete clases de complejidad y en ambos lenguajes. La matriz de confusión es estrictamente diagonal, sin confusiones entre clases adyacentes. Las tres réplicas coincidieron entre sí en los 48 algoritmos, y no se registró ningún error de invocación.

**Corrección de la verdad de terreno.** En la primera puntuación se registraron tres discrepancias de complejidad espacial. Su examen mostró que en los tres casos la estimación del modelo era correcta y el error estaba en la verdad de terreno: `HeapExtractAll` reserva explícitamente un arreglo de salida de tamaño n, de modo que el valor inicial O(1) era factualmente incorrecto, mientras que `FloydWarshall` y `HeapSort` dependían de una convención de espacio no especificada. Se corrigió la entrada errónea, se declaró la convención de espacio auxiliar y se conservó la versión original en `ground_truth_v1_original.csv`.

## Limitaciones

La exactitud del 100 % sobre el corpus canónico debe interpretarse con cautela: son algoritmos ampliamente representados en los datos de entrenamiento de cualquier modelo de lenguaje contemporáneo, de modo que ese subconjunto mide sobre todo el reconocimiento de patrones canónicos y no la capacidad de análisis sobre código novel. El conjunto adversarial se incorporó para mitigar esa limitación, y que la exactitud se mantenga en él —incluida la detección de código inalcanzable y el rechazo de nombres engañosos— es evidencia más fuerte. Aun así, es pequeño (n = 8) y ambos conjuntos se restringen a Java y C#. Una exactitud perfecta sobre un corpus de esta naturaleza indica ausencia de fallo detectable en las condiciones probadas, no ausencia de fallo. La validación sobre código estudiantil real, con sus errores, estilos heterogéneos y estructuras no canónicas, queda como trabajo pendiente.

## Reproducción

```
python validar_bigo.py --proveedor openai --modelo gpt-5.5-2026-04-23 --replicas 3
python evaluar_bigo.py
```

`validar_bigo.py` lee la credencial de la variable de entorno del proveedor (`OPENAI_API_KEY`) y no acepta claves por línea de órdenes ni las escribe en ningún archivo. Los resultados no son bit a bit reproducibles: los proveedores comerciales no garantizan determinismo estricto, motivo por el cual el diseño incorpora réplicas.

## Archivos

- `corpus/java/`, `corpus/csharp/` — los 40 algoritmos canónicos.
- `adversarial/java/`, `adversarial/csharp/` — los 8 casos adversariales.
- `ground_truth.csv`, `ground_truth_adversarial.csv` — verdad de terreno documentada.
- `bigo_prompt.txt` — prompt estandarizado de estimación.
- `validar_bigo.py` — ejecuta la validación contra la API oficial del proveedor.
- `evaluar_bigo.py` — compara predicciones con verdad de terreno y produce las tablas.
