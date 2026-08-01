# Comparación equilibrada frente a Dolos y JPlag — protocolo

Este paquete ejecuta la comparación con los detectores clásicos de forma metodológicamente defendible y **archivable**. Sustituye a cualquier cifra previa: nada se reporta en el manuscrito que no salga de una corrida real cuyas salidas crudas queden depositadas en el repositorio.

## Por qué este protocolo, y no el habitual

Dolos y JPlag son herramientas **de cohorte**. Sus puntajes dependen del conjunto de entregas analizado: Dolos identifica y descuenta el código de plantilla compartido por todo el corpus, y la similitud de JPlag es significativa dentro de un grupo de entregas. Ejecutarlas sobre parejas aisladas de dos archivos desactiva ese mecanismo y no corresponde a cómo se usan en una institución.

Por eso se ejecutan **dos modos** y se reportan por separado:

**Modo cohorte (principal).** Los 60 archivos de cada lenguaje entran como entregas independientes en una sola corrida; después se extraen las similitudes de los 120 pares del estudio. Es el uso real de las herramientas.

**Modo aislado (secundario).** Cada par por separado, que es como suele hacerse en la literatura. La diferencia entre ambos modos es en sí misma un resultado reportable: cuantifica cuánto distorsiona el protocolo a las herramientas.

Además, los pares de la categoría *idéntico* comparan un archivo consigo mismo. Como ninguna herramienta compara una entrega contra sí misma, el script **materializa una copia** con nombre distinto (sufijo `_COPY`), de modo que la comparación exista de verdad en lugar de asumir un 100 %.

## Decisiones que deben fijarse ANTES de ejecutar

Tres, y las tres deben quedar escritas en Métodos:

**Banda de la categoría *diferente*.** El protocolo calcula los resultados con la banda **simétrica** (0–20 %, la misma que se aplicó a los LLM) y también con la **relajada** (0–30 %). La simétrica es la que debe encabezar el reporte; la relajada se incluye por transparencia. No es admisible conceder una banda más ancha solo a una de las partes.

**Tolerancia en la categoría *idéntico*.** Su rango esperado es 100–100, un punto exacto. Los LLM devolvían exactamente 100, pero una herramienta de huellas puede reportar 97–99 para archivos idénticos y «fallar» por un artefacto. Fija una tolerancia a priori con `--tol-identico` (por ejemplo 5) y aplícala **por igual a todas las herramientas**, LLM incluidos, o déjala en 0 y documenta la consecuencia.

**Métrica primaria de cada herramienta.** Dolos: el campo `similarity` de `pairs.csv`. JPlag: la similitud media que exporta. Ambas se escalan a 0–100. Debe constar en el manuscrito qué campo exacto se usó.

## Instalación en Windows

**JPlag** necesita Java 21 o superior (comprueba con `java -version`). Descarga el JAR de las *releases* oficiales del proyecto en GitHub y colócalo junto a estos scripts como `jplag.jar`.

**Dolos** se instala con `npm install -g @dodona/dolos`, que compila analizadores nativos y por tanto requiere herramientas de compilación (en Windows, `npm install -g windows-build-tools` o Visual Studio Build Tools). Si eso da problemas, la vía más limpia es Docker Desktop con la imagen oficial del proyecto.

Verifica ambas antes de seguir: `java -jar jplag.jar --help` y `dolos --version`.

## Ejecución

**Paso 1 — preparar las carpetas de entregas.** Desde la raíz del repositorio:

```powershell
python baselines.py preparar --metadata metadata.csv --repo . --outdir baselines_work
```

Crea `baselines_work/cohorte/{csharp,java}/` con una subcarpeta por entrega, `baselines_work/aislado/<CASE_ID>/` con dos entregas por par, y el mapa `pares.csv`.

**Paso 2 — ejecutar las herramientas.** Modo cohorte, una corrida por lenguaje y herramienta:

```powershell
dolos run -f csv -l csharp -o out_dolos_cs baselines_work\cohorte\csharp
dolos run -f csv -l java   -o out_dolos_java baselines_work\cohorte\java
java -jar jplag.jar baselines_work\cohorte\csharp -l csharp --csv-export -r out_jplag_cs
java -jar jplag.jar baselines_work\cohorte\java   -l java   --csv-export -r out_jplag_java
```

Verifica con `--help` que las claves de lenguaje (`csharp`, `java`) son las que espera tu versión; algunas usan `c-sharp` o `csharp`. Para el modo aislado, itera las carpetas de `baselines_work\aislado\` con los mismos comandos.

**Paso 3 — unificar las salidas.**

```powershell
python baselines.py parsear --pares baselines_work\pares.csv `
  --entrada dolos:cohorte:out_dolos_cs\pairs.csv dolos:cohorte:out_dolos_java\pairs.csv `
            jplag:cohorte:out_jplag_cs\results.csv jplag:cohorte:out_jplag_java\results.csv `
  --out baselines_raw.csv
```

El comando avisa si algún par se queda sin comparación, lo que indica que la herramienta no lo emitió: hay que resolverlo antes de continuar, no ignorarlo.

**Paso 4 — evaluar.**

```powershell
python baselines.py evaluar --in baselines_raw.csv --tol-identico 5
```

Devuelve coincidencia, sensibilidad y especificidad con ambas bandas, el desglose por categoría, y la comparación cohorte vs aislado.

## Qué archivar y qué reportar

En el repositorio deben quedar: `baselines_raw.csv`, las salidas crudas de las herramientas (`pairs.csv`, exportaciones de JPlag), las versiones exactas de cada herramienta, el equipo y las fechas de ejecución. Sin eso, la comparación no es citable.

En el manuscrito, la tabla principal debe usar la **banda simétrica** y el **modo cohorte**, con el modo aislado como análisis secundario. La comparación de tiempos entre herramientas locales y APIs remotas no debe presentarse en la misma tabla sin advertir explícitamente que no son magnitudes comparables: unas se ejecutan en la máquina y las otras incluyen latencia de red.

Y una precaución de interpretación que conviene escribir: la similitud que devuelven Dolos y JPlag es solapamiento de huellas o cobertura de *tokens*, no un compuesto ponderado de dimensiones funcional, estructural, léxica y estilística. Evaluar ambas contra la misma banda compara constructos distintos, y esa limitación debe reconocerse en lugar de disimularse.
