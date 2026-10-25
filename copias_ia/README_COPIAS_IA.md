# Copias reescritas con IA (revisión M1)

Esta carpeta añade al benchmark el caso que más preocupa a un docente: un estudiante toma el programa de otro y le pide a un modelo de lenguaje que lo "disfrace". La pregunta que se responde es si cada sistema separa esas copias de las **soluciones independientes del mismo ejercicio** (los 30 pares `functional`, clones tipo 4).

## Diseño

| Elemento | Decisión |
|---|---|
| Programas de partida | Los 30 programas de referencia (`CODE_IDENT_*`), 15 en C# y 15 en Java |
| Niveles de reescritura | **Ligera**: nombres, comentarios y orden. **Intensa**: además, estructura (bucles, división de métodos, estructuras de datos) |
| Copias | 60 (30 × 2 niveles): `CODE_IAL_*` (ligera) y `CODE_IAI_*` (intensa) |
| Generadores | Recomendado: un modelo abierto ejecutado en local (Ollama), que no está entre los evaluados, y opcionalmente uno comercial. Se reparten en rotación |
| Temperatura de generación | 0.7 (uso normal de un estudiante) |
| Control de calidad | Cada copia se compila y ejecuta con 3 conjuntos de entrada; solo entran las que imprimen exactamente lo mismo que el original |
| Negativos | Los 30 pares `functional`, re-evaluados en la misma sesión (`_R2`) para comparar con la misma versión de cada modelo |
| Evaluación | Los 4 modelos × 3 réplicas con el mismo prompt (`prompt.txt`) y Moss, JPlag y Dolos en modo cohorte |
| Medida principal | AUC copia-IA frente a solución independiente, con IC 95 % por remuestreo de programas de referencia; tasas de detección y de falsos positivos a umbrales 50/70/80/90 |

## Volumen y costo

| Paso | Llamadas a API comerciales |
|---|---|
| Generación con Ollama (local) | 0 |
| Generación con un modelo comercial (si se usa) | ~30–60 (más regeneraciones) |
| Evaluación: 90 pares × 4 modelos × 3 réplicas | 1 080 |
| Opcional `--con-estructurales` (+30 pares de anclaje) | +360 |

La nueva versión de `benchmark_replicas.py` registra los tokens de entrada y salida de cada llamada (`input_tokens`, `output_tokens`), con lo que el costo queda documentado.

## Requisitos (Windows)

- Python 3.10+ con `pandas`, `numpy` y `scipy`.
- .NET SDK 8 (`dotnet --version`) y JDK 17+ (`javac -version`).
- Ollama (https://ollama.com) con un modelo de código, p. ej. `ollama pull qwen2.5-coder:14b`.
- Claves de API **nuevas** en variables de entorno (nunca en archivos): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`.
- Para Moss: su propio cliente `moss` (ver `ejecutar_moss.sh`) y WSL.

## Pasos (PowerShell, desde la carpeta `SimilCode-Benchmark`)

```powershell
# 1. Generar las 60 copias (ejemplo: modelo local + uno comercial)
python copias_ia/generar_copias_ia.py --generadores ollama:qwen2.5-coder:14b

# 2. Verificar que cada copia hace exactamente lo mismo que el original
python copias_ia/verificar_equivalencia.py
#    Regenerar las que fallen, p. ej.:
python copias_ia/generar_copias_ia.py --generadores ollama:qwen2.5-coder:14b --solo CODE_IAI_CS_004
python copias_ia/verificar_equivalencia.py --solo CODE_IAI_CS_004

# 3. Construir los casos de la segunda corrida
python copias_ia/construir_casos_ia.py

# 4. Evaluar con los cuatro modelos (mismo prompt y modelos que en el estudio)
python benchmark_replicas.py run --cases metadata_ia.csv --prompt prompt.txt `
    --replicas 3 --only openai,deepseek,gemini,anthropic --out copias_ia/resultados_replicas_ia.csv

# 5. Detectores clásicos en modo cohorte (carpeta aparte: no toca la corrida original)
python baselines.py preparar --metadata metadata_ia.csv --outdir baselines_work_ia
java -jar jplag.jar baselines_work_ia\cohorte\csharp -l csharp -r out_jplag_cs_ia --csv-export --max-comparisons -1
java -jar jplag.jar baselines_work_ia\cohorte\java   -l java   -r out_jplag_java_ia --csv-export --max-comparisons -1
dolos run -f csv -l csharp -o out_dolos_cs_ia baselines_work_ia\cohorte\csharp\*\*.cs
dolos run -f csv -l java   -o out_dolos_java_ia baselines_work_ia\cohorte\java\*\*.java
wsl bash -c "TRABAJO=baselines_work_ia/cohorte SUFIJO=_ia bash ejecutar_moss.sh"
python baselines.py parsear --pares baselines_work_ia/pares.csv `
    --entrada jplag:cohorte:RUTA_CSV_JPLAG_CS_IA jplag:cohorte:RUTA_CSV_JPLAG_JAVA_IA `
              dolos:cohorte:out_dolos_cs_ia\pairs.csv dolos:cohorte:out_dolos_java_ia\pairs.csv `
              moss:cohorte:moss_cs_ia.html moss:cohorte:moss_java_ia.html `
    --out copias_ia/baselines_raw_ia.csv --faltantes-cero

# 6. Análisis
python copias_ia/analisis_copias_ia.py
```

## Qué se archiva

`copias_ia/` completo: prompts de reescritura, `copias_ia_log.csv` (modelo, versión, fecha, tokens y hash del prompt de cada copia), `respuestas/` (respuesta íntegra del generador), `equivalencia*.csv`, `resultados_replicas_ia.csv`, `baselines_raw_ia.csv` y `resultados_copias_ia.json`; además `metadata_ia.csv` (en la raíz) y las copias `csharp/CODE_IA*` y `java/CODE_IA*`.

## Advertencias

- No use las claves que estuvieron en `ejecutar_benchmark.ps1`: deben estar revocadas.
- No publique el archivo `moss` (contiene su identificador).
- Los modelos con alias (`claude-opus-5`, `deepseek-v4-pro`, `gemini-3.1-pro-preview`) pueden haber cambiado desde julio de 2026; por eso los negativos se re-evalúan en la misma sesión y el análisis informa la deriva.
