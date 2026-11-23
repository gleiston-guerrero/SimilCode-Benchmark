# Experimentos pendientes (no ejecutados)

Estos experimentos responden a debilidades que no se pueden corregir solo con los datos archivados. Ninguno se ha ejecutado; ningún número del manuscrito procede de ellos.

| Archivo | Qué comprueba | Qué requiere |
|---|---|---|
| `prompt_derivacion.txt`, `evaluar_derivacion.py` | Comprobación fuera de muestra de la puntuación de derivación: el modelo recibe las cinco dimensiones definidas y se le pregunta directamente la probabilidad de que B derive de A. Hipótesis fijadas antes de ejecutar en el docstring (H1: AUC ≥ 0.90 en copias convencionales; H2: AUC < 0.80 en copias de modelos comerciales). | Claves de API de los cuatro proveedores; 90 pares × 4 modelos × 3 réplicas = 1 080 llamadas. |
| `ejecutar_nicad.sh`, `nicad_resultados.py` | NiCad 7 como cuarto detector clásico (detector de clones casi idénticos basado en normalización), sobre las mismas cohortes. | WSL con gcc y make; descarga OpenTxl 11.3.7 y NiCad. La sesión de análisis no pudo ejecutar binarios descargados. |

Orden recomendado: `python experimentos_pendientes\evaluar_derivacion.py run`, luego `analyze`; `bash experimentos_pendientes/ejecutar_nicad.sh` en WSL. Los resultados se guardan en esta carpeta (`resultados_derivacion.csv/.json`, `nicad_similitud.csv`).
