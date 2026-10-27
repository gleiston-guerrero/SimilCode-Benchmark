# Copias reescritas con IA generativa (segunda corrida)

Esta carpeta documenta la segunda corrida del benchmark: copias de los 30 programas de referencia reescritas por modelos de lenguaje con el encargo de disimular el plagio, verificadas por ejecución y puntuadas, junto con las soluciones independientes del mismo ejercicio, por los cuatro modelos evaluados y por Moss, JPlag y Dolos. En los nombres de algunos scripts y notas aparece la etiqueta interna «M1», que identifica esta segunda corrida.

## Conjuntos de copias

| Conjunto | Archivos | Generador | Prompt | Fecha | Conservadas |
|---|---|---|---|---|---|
| Local, reescritura ligera | `csharp/CODE_IAL_*`, `java/CODE_IAL_*` | `qwen2.5-coder:14b` (Ollama, local), temperatura 0.7 | `prompt_reescritura_ligera.txt` | 24-10-2026 | 26 de 30 |
| Local, reescritura intensa | `csharp/CODE_IAI_*`, `java/CODE_IAI_*` | ídem | `prompt_reescritura_intensa.txt` | 24-10-2026 | 28 de 30 |
| Modelos comerciales, reescritura intensa | `csharp/CODE_IAP_*`, `java/CODE_IAP_*` | Gemini 3.1 Pro (15), DeepSeek-V4-pro (10), Claude Opus 5 (5), temperatura 0.7 | `prompt_reescritura_api.txt` (idéntico al intenso) | 25-10-2026 | 30 de 30 |

- **Primer intento (23–24-10-2026).** Una primera versión de los prompts (`prompts_v1/`) exigía la misma salida, pero no mencionaba expresamente los textos impresos; los modelos reformularon títulos y mensajes y solo 14 de 60 copias locales superaron la verificación. Los prompts se revisaron (versión actual) y las 60 copias se generaron de nuevo. El hash SHA-256 de cada prompt figura en `copias_ia_log.csv` (`52ecdb8f…` y `6cd4289f…` para la versión 1; `34c8b8dc…` y `84117838…` para la versión revisada).
- **Copias de modelos comerciales.** Se pidieron por turnos a GPT-5.5, Claude Opus 5, Gemini 3.1 Pro y DeepSeek-V4-pro. GPT-5.5 rechazó las 8 solicitudes que recibió y Claude Opus 5, 3 de 8 (`rechazos_ia.csv`; las respuestas de rechazo están en `respuestas/`). Las 8 rechazadas por GPT-5.5 se pidieron de nuevo, con el mismo prompt, a Gemini 3.1 Pro, y las 3 rechazadas por Claude Opus 5, a DeepSeek-V4-pro.

## Verificación de equivalencia

`verificar_equivalencia.py` compila cada copia y su original (C#: .NET SDK 8; Java: JDK) y los ejecuta con tres conjuntos de entrada por teclado; normaliza finales de línea y espacios finales y, si un programa sigue esperando datos a los 15 s, compara la salida producida hasta entonces. Las copias que fallaron se regeneraron hasta tres veces (`generar_copias_ia.py --solo` / `--solo-fallidas`). El programa `JAVA_007` imprime números aleatorios: sus tres copias se revisaron a mano (`marcar_revision_manual.py`; motivo y revisor en la columna `nota` de `equivalencia_resumen.csv`). Las seis copias locales excluidas (`IAL_CS_009/010/013/015`, `IAI_CS_010/015`) cambiaban el título impreso en todos los intentos (`equivalencia.csv`, columna `detail`).

## Puntuación (25-10-2026)

- `../metadata_ia.csv`: 114 pares = 84 copias conservadas + los 30 pares `functional` re-evaluados en la misma sesión (sufijo `_R2`).
- `res_<proveedor>.csv` y su unión `resultados_replicas_ia.csv`: mismo prompt (`../prompt.txt`), modelos y configuración que la primera corrida, tres réplicas; 1 366 de 1 368 respuestas con puntuación global analizable. Las llamadas fallidas (211 a GPT-5.5 por saldo agotado; 36 a Gemini 3.1 Pro por errores de autenticación o cuota) se conservan con la columna `error` rellena y se repitieron hasta obtener respuesta. `log_eval_*.txt`: salida de consola de cada ejecución (UTF-16).
- Detectores clásicos sobre la cohorte completa (69 entregas en C# y 75 en Java): `../out_jplag_*_ia/` (JPlag 6.3.0, `--csv-export --mode RUN`), `../out_dolos_*_ia/` (Dolos 2.9.3 en WSL, valores por defecto), `../moss_*_ia.html` (Moss, `-d -m 10 -n 1000`; 44 pares sin comparación registrados como 0) y su unión `baselines_raw_ia.csv`.
- `../out_dolos_*_ia_r1/` y `resultados_copias_ia_local_qwen.json` corresponden a un análisis intermedio, sobre la cohorte sin las copias de modelos comerciales; no se informan en el manuscrito, y el informe de Moss de esa cohorte fue sustituido por el definitivo.

## Reproducir el análisis (sin llamadas a API)

```bash
pip install pandas numpy scipy
python analisis_tipos_clon.py              # Tabla 1: copias convencionales frente a soluciones independientes
python copias_ia/analisis_copias_ia.py     # Tabla 2: copias reescritas con IA -> copias_ia/resultados_copias_ia.json
python copias_ia/similitud_tokens_ia.py    # similitud de tokens normalizada de cada par -> copias_ia/similitud_tokens_ia.csv
```

## Regenerar la corrida completa

Requiere Ollama, .NET SDK 8, JDK 21+, claves de API en variables de entorno (nunca en archivos), `jplag.jar`, Dolos 2.9.3 y un cliente `moss` propio (no se versiona). Los pasos están automatizados en `ejecutar_paso3.ps1`; las respuestas de los modelos comerciales no son deterministas, por lo que una nueva corrida no reproducirá exactamente los mismos textos ni puntuaciones.
