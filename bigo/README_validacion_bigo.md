# Validación del componente de estimación Big O (M5)

Este paquete valida empíricamente el estimador de complejidad algorítmica de SimilCode frente a un conjunto curado de algoritmos con complejidad documentada. Responde a la preocupación mayor sobre un componente que figura en el título del manuscrito y que hasta ahora se presentaba sin validación.

## Diseño

**Corpus canónico (40 algoritmos).** 20 en Java y 20 en C#, balanceados en siete clases de complejidad temporal de peor caso: O(1) — 4 casos; O(log n) — 6; O(n) — 9; O(n log n) — 4; O(n²) — 10; O(n³) — 3; O(2ⁿ) — 4. Incluye búsquedas, ordenamientos, recorridos de grafos sobre matriz de adyacencia, programación dinámica y recursión exponencial.

**Conjunto adversarial (8 casos).** Diseñado para que el corpus discrimine y no se limite a medir el reconocimiento de algoritmos de libro de texto: nombres y comentarios que contradicen la estructura real, anidamiento aparente con cota interna constante, bucles secuenciales que no se multiplican, memoización que colapsa una recursión binaria, código muerto de orden superior y división sucesiva disfrazada de recorrido lineal.

**Verdad de terreno.** Complejidad temporal de **peor caso**, con las siete clases anteriores. Para el espacio se adopta la convención de **espacio auxiliar** (excluye la estructura de entrada, incluye la pila de recursión), declarada explícitamente en `ground_truth.csv`. Las fuentes se documentan por entrada; los resultados estándar provienen de Cormen et al. (2022), *Introduction to Algorithms*, 4.ª ed., y de Knuth para el algoritmo de Euclides.

**Procedimiento de clasificación.** Cada fragmento se evalúa de forma independiente con el prompt estandarizado `bigo_prompt.txt` (Chain-of-Thought + Chain-of-Verification, en la misma línea metodológica que el prompt de similitud). El evaluador es ciego: recibe únicamente el código, nunca la complejidad documentada ni el nombre del archivo de verdad de terreno, que se almacena en un árbol de directorios separado.

## Resultados

| Conjunto | n | Exactitud temporal | Exactitud espacial |
|---|---|---|---|
| Canónico | 40 | 100.0 % (40/40) | 100.0 % (40/40) |
| Adversarial | 8 | 100.0 % (8/8) | 100.0 % (8/8) |
| **Total** | **48** | **100.0 %** | **100.0 %** |

La exactitud es del 100 % en cada una de las siete clases de complejidad y en ambos lenguajes (Java 20/20, C# 20/20). La matriz de confusión es estrictamente diagonal, sin ninguna confusión entre clases adyacentes.

**Corrección de la verdad de terreno.** En la primera puntuación se registraron tres discrepancias de complejidad espacial. Su examen mostró que en los tres casos la estimación del modelo era correcta y el error estaba en la verdad de terreno: `HeapExtractAll` reserva explícitamente un arreglo de salida de tamaño n (el valor inicial O(1) era factualmente incorrecto), mientras que `FloydWarshall` y `HeapSort` dependían de una convención de espacio no especificada. Se corrigió la entrada errónea, se declaró la convención de espacio auxiliar y se conservó la versión original en `ground_truth_v1_original.csv` para trazabilidad. Ambas cifras se reportan de forma transparente: 92.5 % bajo la verdad de terreno original y 100 % tras la corrección documentada.

## Limitaciones

La exactitud del 100 % sobre el corpus canónico debe interpretarse con cautela: son algoritmos de libro de texto ampliamente representados en los datos de entrenamiento de cualquier modelo de lenguaje contemporáneo, de modo que ese subconjunto mide principalmente el **reconocimiento de patrones canónicos** y no la capacidad de análisis sobre código novel. El conjunto adversarial se incorporó precisamente para mitigar esa limitación, y el hecho de que la exactitud se mantenga en él —incluida la detección de código muerto y el rechazo de nombres engañosos— constituye evidencia más fuerte. Aun así, el conjunto adversarial es pequeño (n = 8) y ambos conjuntos están restringidos a Java y C#. La validación sobre código estudiantil real, con sus errores, estilos heterogéneos y estructuras no canónicas, queda como trabajo pendiente.

## Archivos

- `corpus/java/`, `corpus/csharp/` — los 40 algoritmos canónicos.
- `adversarial/java/`, `adversarial/csharp/` — los 8 casos adversariales.
- `ground_truth.csv`, `ground_truth_adversarial.csv` — verdad de terreno documentada.
- `ground_truth_v1_original.csv` — versión previa a la corrección, para trazabilidad.
- `bigo_prompt.txt` — prompt estandarizado de estimación.
- `predicciones_opus5.csv`, `predicciones_adversarial_opus5.csv` — clasificaciones obtenidas.
- `resultados_bigo.csv`, `resultados_bigo_adversarial.csv` — comparación caso a caso.
- `validar_bigo.py` — ejecuta la validación contra la API oficial.
- `evaluar_bigo.py` — calcula exactitud y matrices de confusión.

## Reproducción contra la API oficial

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python validar_bigo.py --corpus corpus --prompt bigo_prompt.txt --out predicciones_api.csv
python evaluar_bigo.py --pred predicciones_api.csv --truth ground_truth.csv --out resultados_bigo.csv
```

Para el conjunto adversarial se sustituye `--corpus adversarial` y `--truth ground_truth_adversarial.csv`.
