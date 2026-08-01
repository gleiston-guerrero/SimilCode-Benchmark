# Protocolo para JPlag y Dolos

Mismo diseño que se aplicó a Moss: **modo cohorte** (todas las entregas del lenguaje en una sola corrida) como resultado principal, con las mismas bandas y las mismas decisiones declaradas. Empieza por JPlag, que es la más sencilla de instalar.

---

## Parte 1 — JPlag

### Instalación

Comprueba primero la versión de Java en PowerShell:

```powershell
java -version
```

JPlag 6 requiere **Java 21 o superior**. Si tienes una versión anterior, instala un JDK 21 (por ejemplo Temurin de Adoptium) antes de continuar.

Descarga el JAR desde las *releases* oficiales del proyecto en GitHub — el archivo que necesitas es el que incluye las dependencias, con un nombre del tipo `jplag-6.x.x-jar-with-dependencies.jar`. Guárdalo en la raíz del repositorio y **renómbralo a `jplag.jar`** para que los comandos siguientes funcionen tal cual.

Verifica que arranca:

```powershell
java -jar jplag.jar --help
```

Debe mostrar la lista de opciones, entre ellas `-l`, `-r` y `--csv-export`.

### Ejecución

Desde la raíz del repositorio, en PowerShell, una corrida por lenguaje, capturando el log completo porque lo vamos a necesitar:

```powershell
java -jar jplag.jar baselines_work\cohorte\csharp -l csharp -r out_jplag_cs --csv-export --max-comparisons -1 2>&1 | Tee-Object -FilePath jplag_cs.log
java -jar jplag.jar baselines_work\cohorte\java   -l java   -r out_jplag_java --csv-export --max-comparisons -1 2>&1 | Tee-Object -FilePath jplag_java.log
```

`--max-comparisons -1` desactiva el truncamiento del informe: por defecto JPlag solo conserva los pares más similares, y varios de nuestros 120 pares están en la cola baja de la distribución.

JPlag produce un archivo comprimido `out_jplag_cs.jplag` y, gracias a `--csv-export`, un CSV con las similitudes por pares. Localiza ese CSV:

```powershell
Get-ChildItem -Recurse -Filter *.csv | Where-Object { $_.Name -notlike "metadata*" -and $_.Name -notlike "results_*" } | Select-Object FullName, Length
```

Anota su ruta exacta: la necesitarás en el parseo. Si no aparece ningún CSV, no pasa nada — el parser también lee el archivo `.jplag` directamente.

### Fallos de análisis sintáctico (ANTLR)

En la corrida de C# la gramática de JPlag emitió errores de análisis sobre buena parte del corpus: `new()` con tipo inferido, `async`/`await`/`Task`, literales decimales (`0.03m`), cadenas interpoladas con especificador de formato, e inicializadores de propiedades automáticas. Cuando el análisis falla, JPlag no se detiene: tokeniza de forma incompleta y sigue adelante, de modo que **la similitud de esas entregas no es fiable**.

Eso no invalida el ejercicio; es un hallazgo por derecho propio sobre la cobertura sintáctica de una herramienta clásica frente a código contemporáneo. Pero hay que medirlo, no describirlo:

```powershell
python baselines.py antlr --log jplag_cs.log   --pares baselines_work\pares.csv --out antlr_cs.csv
python baselines.py antlr --log jplag_java.log --pares baselines_work\pares.csv --out antlr_java.csv
```

La salida da tres cifras que van a Métodos y a Limitaciones: cuántas entregas de las 75 fallaron el análisis, cuántos de los 120 pares tienen al menos una entrega afectada, y el desglose por categoría. Si la proporción es alta, la comparación con JPlag debe reportarse dos veces: sobre todos los pares y sobre el subconjunto no afectado.

### Una decisión que debe constar en Métodos

JPlag emite dos métricas por par, `AVG` y `MAX`. El parser toma **siempre `AVG`**, la media de las dos similitudes direccionales, porque es la magnitud simétrica comparable con la `similarity` de Dolos y con la media de los dos porcentajes de Moss. Usar `MAX` produciría cifras sistemáticamente más altas y una comparación desigual entre herramientas.

---

## Parte 2 — Dolos

Dolos es la más incómoda de instalar en Windows porque compila analizadores nativos. Prueba las vías en este orden y quédate con la primera que funcione.

### Vía A — npm

```powershell
node --version
npm install -g @dodona/dolos
dolos --version
```

Si la instalación falla con errores de `node-gyp`, faltan herramientas de compilación: instala **Visual Studio Build Tools** con la carga de trabajo «Desarrollo para escritorio con C++» y repite. Si tampoco así, pasa a la vía B.

### Vía B — Docker

Instala Docker Desktop, y luego:

```powershell
docker run --rm -v "${PWD}:/dolos" ghcr.io/dodona-edu/dolos-cli --version
```

En esta vía, cada comando `dolos` se sustituye por ese `docker run` completo, y las rutas se escriben tal como las ve el contenedor (`/dolos/...`).

### Claves de lenguaje

La documentación de Dolos no publica los identificadores exactos del parámetro `-l`. Averígualos antes de ejecutar:

```powershell
dolos run --help
```

Busca en la ayuda los valores admitidos. Para C# suele ser `c-sharp` o `csharp`, y para Java, `java`. **Confirma cuál acepta tu versión y anótalo**, porque debe constar en Métodos.

### Ejecución

```powershell
dolos run -f csv -l csharp -o out_dolos_cs baselines_work\cohorte\csharp\*\*.cs
dolos run -f csv -l java   -o out_dolos_java baselines_work\cohorte\java\*\*.java
```

Si tu versión no admite `-o`, omítelo: Dolos creará un directorio de salida en la carpeta actual. En cualquier caso, el archivo que interesa es **`pairs.csv`**:

```powershell
Get-ChildItem -Recurse -Filter pairs.csv | Select-Object FullName, Length
```

Un detalle importante: si PowerShell no expande el comodín `*\*.cs`, expándelo tú y pasa la lista:

```powershell
$archivos = Get-ChildItem baselines_work\cohorte\csharp\*\*.cs | ForEach-Object { $_.FullName }
dolos run -f csv -l csharp -o out_dolos_cs $archivos
```

---

## Parte 3 — Integrar las tres herramientas

Con las salidas de JPlag y Dolos ya generadas, y los HTML de Moss que ya tienes:

```powershell
python baselines.py parsear --pares baselines_work\pares.csv `
  --entrada moss:cohorte:moss_cs.html moss:cohorte:moss_java.html `
            jplag:cohorte:RUTA_DEL_CSV_DE_JPLAG_CS jplag:cohorte:RUTA_DEL_CSV_DE_JPLAG_JAVA `
            dolos:cohorte:out_dolos_cs\pairs.csv dolos:cohorte:out_dolos_java\pairs.csv `
  --out baselines_raw.csv --faltantes-cero

python baselines.py evaluar --in baselines_raw.csv --tol-identico 5
```

Fíjate en dos cosas de la salida del `parsear`: cuántas comparaciones leyó de cada archivo (si alguna da 0, el formato no se reconoció) y cuántos pares quedaron sin comparación por herramienta. Ese segundo número es un resultado en sí mismo: en Moss fueron 55 de 120.

---

## Qué anotar mientras ejecutas

Cuatro datos por herramienta, que van directos a Métodos: la **versión exacta** (`java -jar jplag.jar --version`, `dolos --version`), la **clave de lenguaje** que aceptó, la **fecha y hora** de ejecución, y el **equipo** donde corrió. Sin eso la comparación no es citable.

---

## Advertencia que ya conocemos por Moss

Moss nunca devolvió 100 % para archivos idénticos byte a byte: su rango fue 79–99. Es muy probable que JPlag y Dolos presenten el mismo desfase, porque las tres miden cobertura de coincidencia y no una similitud calibrada donde idéntico equivalga a 100.

Por eso, cuando tengamos las tres, **la tabla principal del manuscrito debe construirse sobre el patrón por categoría y las distribuciones de similitud**, no sobre el porcentaje agregado de coincidencia — que, como comprobamos, varía 25 puntos según la tolerancia que se elija para la categoría idéntico. La comparación honesta es cualitativa en su estructura y cuantitativa en cada categoría, no un ranking global.
