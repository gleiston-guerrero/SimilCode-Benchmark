# ComparaciÃ³n equilibrada frente a Dolos y JPlag â€” protocolo

Este paquete ejecuta la comparaciÃ³n con los detectores clÃ¡sicos de forma metodolÃ³gicamente defendible y **archivable**. Sustituye a cualquier cifra previa: nada se reporta en el manuscrito que no salga de una corrida real cuyas salidas crudas queden depositadas en el repositorio.

## Por quÃ© este protocolo, y no el habitual

Dolos y JPlag son herramientas **de cohorte**. Sus puntajes dependen del conjunto de entregas analizado: Dolos identifica y descuenta el cÃ³digo de plantilla compartido por todo el corpus, y la similitud de JPlag es significativa dentro de un grupo de entregas. Ejecutarlas sobre parejas aisladas de dos archivos desactiva ese mecanismo y no corresponde a cÃ³mo se usan en una instituciÃ³n.

Por eso se ejecutan **dos modos** y se reportan por separado:

**Modo cohorte (principal).** Los 60 archivos de cada lenguaje entran como entregas independientes en una sola corrida; despuÃ©s se extraen las similitudes de los 120 pares del estudio. Es el uso real de las herramientas.

**Modo aislado (secundario).** Cada par por separado, que es como suele hacerse en la literatura. La diferencia entre ambos modos es en sÃ­ misma un resultado reportable: cuantifica cuÃ¡nto distorsiona el protocolo a las herramientas.

AdemÃ¡s, los pares de la categorÃ­a *idÃ©ntico* comparan un archivo consigo mismo. Como ninguna herramienta compara una entrega contra sÃ­ misma, el script **materializa una copia** con nombre distinto (sufijo `_COPY`), de modo que la comparaciÃ³n exista de verdad en lugar de asumir un 100 %.

## Decisiones que deben fijarse ANTES de ejecutar

Tres, y las tres deben quedar escritas en MÃ©todos:

**Banda de la categorÃ­a *diferente*.** El protocolo calcula los resultados con la banda **simÃ©trica** (0â€“20 %, la misma que se aplicÃ³ a los LLM) y tambiÃ©n con la **relajada** (0â€“30 %). La simÃ©trica es la que debe encabezar el reporte; la relajada se incluye por transparencia. No es admisible conceder una banda mÃ¡s ancha solo a una de las partes.

**Tolerancia en la categorÃ­a *idÃ©ntico*.** Su rango esperado es 100â€“100, un punto exacto. Los LLM devolvÃ­an exactamente 100, pero una herramienta de huellas puede reportar 97â€“99 para archivos idÃ©nticos y Â«fallarÂ» por un artefacto. Fija una tolerancia a priori con `--tol-identico` (por ejemplo 5) y aplÃ­cala **por igual a todas las herramientas**, LLM incluidos, o dÃ©jala en 0 y documenta la consecuencia.

**MÃ©trica primaria de cada herramienta.** Dolos: el campo `similarity` de `pairs.csv`. JPlag: la similitud media que exporta. Ambas se escalan a 0â€“100. Debe constar en el manuscrito quÃ© campo exacto se usÃ³.

## InstalaciÃ³n en Windows

**JPlag** necesita Java 21 o superior (comprueba con `java -version`). Descarga el JAR de las *releases* oficiales del proyecto en GitHub y colÃ³calo junto a estos scripts como `jplag.jar`.

**Dolos** se instala con `npm install -g @dodona/dolos`, que compila analizadores nativos y por tanto requiere herramientas de compilaciÃ³n (en Windows, `npm install -g windows-build-tools` o Visual Studio Build Tools). Si eso da problemas, la vÃ­a mÃ¡s limpia es Docker Desktop con la imagen oficial del proyecto.

Verifica ambas antes de seguir: `java -jar jplag.jar --help` y `dolos --version`.

## EjecuciÃ³n

**Paso 1 â€” preparar las carpetas de entregas.** Desde la raÃ­z del repositorio:

```powershell
python baselines.py preparar --metadata metadata.csv --repo . --outdir baselines_work
```

Crea `baselines_work/cohorte/{csharp,java}/` con una subcarpeta por entrega, `baselines_work/aislado/<CASE_ID>/` con dos entregas por par, y el mapa `pares.csv`.

**Paso 2 â€” ejecutar las herramientas.** Modo cohorte, una corrida por lenguaje y herramienta:

```powershell
dolos run -f csv -l csharp -o out_dolos_cs baselines_work\cohorte\csharp
dolos run -f csv -l java   -o out_dolos_java baselines_work\cohorte\java
java -jar jplag.jar baselines_work\cohorte\csharp -l csharp --csv-export -r out_jplag_cs
java -jar jplag.jar baselines_work\cohorte\java   -l java   --csv-export -r out_jplag_java
```

Verifica con `--help` que las claves de lenguaje (`csharp`, `java`) son las que espera tu versiÃ³n; algunas usan `c-sharp` o `csharp`. Para el modo aislado, itera las carpetas de `baselines_work\aislado\` con los mismos comandos.

**Paso 3 â€” unificar las salidas.**

```powershell
python baselines.py parsear --pares baselines_work\pares.csv `
  --entrada dolos:cohorte:out_dolos_cs\pairs.csv dolos:cohorte:out_dolos_java\pairs.csv `
            jplag:cohorte:out_jplag_cs\results.csv jplag:cohorte:out_jplag_java\results.csv `
  --out baselines_raw.csv
```

El comando avisa si algÃºn par se queda sin comparaciÃ³n, lo que indica que la herramienta no lo emitiÃ³: hay que resolverlo antes de continuar, no ignorarlo.

**Paso 4 â€” evaluar.**

```powershell
python baselines.py evaluar --in baselines_raw.csv --tol-identico 5
```

Devuelve coincidencia, sensibilidad y especificidad con ambas bandas, el desglose por categorÃ­a, y la comparaciÃ³n cohorte vs aislado.

## QuÃ© archivar y quÃ© reportar

En el repositorio deben quedar: `baselines_raw.csv`, las salidas crudas de las herramientas (`pairs.csv`, exportaciones de JPlag), las versiones exactas de cada herramienta, el equipo y las fechas de ejecuciÃ³n. Sin eso, la comparaciÃ³n no es citable.

En el manuscrito, la tabla principal debe usar la **banda simÃ©trica** y el **modo cohorte**, con el modo aislado como anÃ¡lisis secundario. La comparaciÃ³n de tiempos entre herramientas locales y APIs remotas no debe presentarse en la misma tabla sin advertir explÃ­citamente que no son magnitudes comparables: unas se ejecutan en la mÃ¡quina y las otras incluyen latencia de red.

Y una precauciÃ³n de interpretaciÃ³n que conviene escribir: la similitud que devuelven Dolos y JPlag es solapamiento de huellas o cobertura de *tokens*, no un compuesto ponderado de dimensiones funcional, estructural, lÃ©xica y estilÃ­stica. Evaluar ambas contra la misma banda compara constructos distintos, y esa limitaciÃ³n debe reconocerse en lugar de disimularse.
