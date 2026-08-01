# Protocolo para JPlag y Dolos

Mismo diseÃ±o que se aplicÃ³ a Moss: **modo cohorte** (todas las entregas del lenguaje en una sola corrida) como resultado principal, con las mismas bandas y las mismas decisiones declaradas. Empieza por JPlag, que es la mÃ¡s sencilla de instalar.

---

## Parte 1 â€” JPlag

### InstalaciÃ³n

Comprueba primero la versiÃ³n de Java en PowerShell:

```powershell
java -version
```

JPlag 6 requiere **Java 21 o superior**. Si tienes una versiÃ³n anterior, instala un JDK 21 (por ejemplo Temurin de Adoptium) antes de continuar.

Descarga el JAR desde las *releases* oficiales del proyecto en GitHub â€” el archivo que necesitas es el que incluye las dependencias, con un nombre del tipo `jplag-6.x.x-jar-with-dependencies.jar`. GuÃ¡rdalo en la raÃ­z del repositorio y **renÃ³mbralo a `jplag.jar`** para que los comandos siguientes funcionen tal cual.

Verifica que arranca:

```powershell
java -jar jplag.jar --help
```

Debe mostrar la lista de opciones, entre ellas `-l`, `-r` y `--csv-export`.

### EjecuciÃ³n

Desde la raÃ­z del repositorio, en PowerShell, una corrida por lenguaje, capturando el log completo porque lo vamos a necesitar:

```powershell
java -jar jplag.jar baselines_work\cohorte\csharp -l csharp -r out_jplag_cs --csv-export --max-comparisons -1 2>&1 | Tee-Object -FilePath jplag_cs.log
java -jar jplag.jar baselines_work\cohorte\java   -l java   -r out_jplag_java --csv-export --max-comparisons -1 2>&1 | Tee-Object -FilePath jplag_java.log
```

`--max-comparisons -1` desactiva el truncamiento del informe: por defecto JPlag solo conserva los pares mÃ¡s similares, y varios de nuestros 120 pares estÃ¡n en la cola baja de la distribuciÃ³n.

JPlag produce un archivo comprimido `out_jplag_cs.jplag` y, gracias a `--csv-export`, un CSV con las similitudes por pares. Localiza ese CSV:

```powershell
Get-ChildItem -Recurse -Filter *.csv | Where-Object { $_.Name -notlike "metadata*" -and $_.Name -notlike "results_*" } | Select-Object FullName, Length
```

Anota su ruta exacta: la necesitarÃ¡s en el parseo. Si no aparece ningÃºn CSV, no pasa nada â€” el parser tambiÃ©n lee el archivo `.jplag` directamente.

### Fallos de anÃ¡lisis sintÃ¡ctico (ANTLR)

En la corrida de C# la gramÃ¡tica de JPlag emitiÃ³ errores de anÃ¡lisis sobre buena parte del corpus: `new()` con tipo inferido, `async`/`await`/`Task`, literales decimales (`0.03m`), cadenas interpoladas con especificador de formato, e inicializadores de propiedades automÃ¡ticas. Cuando el anÃ¡lisis falla, JPlag no se detiene: tokeniza de forma incompleta y sigue adelante, de modo que **la similitud de esas entregas no es fiable**.

Eso no invalida el ejercicio; es un hallazgo por derecho propio sobre la cobertura sintÃ¡ctica de una herramienta clÃ¡sica frente a cÃ³digo contemporÃ¡neo. Pero hay que medirlo, no describirlo:

```powershell
python baselines.py antlr --log jplag_cs.log   --pares baselines_work\pares.csv --out antlr_cs.csv
python baselines.py antlr --log jplag_java.log --pares baselines_work\pares.csv --out antlr_java.csv
```

La salida da tres cifras que van a MÃ©todos y a Limitaciones: cuÃ¡ntas entregas de las 75 fallaron el anÃ¡lisis, cuÃ¡ntos de los 120 pares tienen al menos una entrega afectada, y el desglose por categorÃ­a. Si la proporciÃ³n es alta, la comparaciÃ³n con JPlag debe reportarse dos veces: sobre todos los pares y sobre el subconjunto no afectado.

### Una decisiÃ³n que debe constar en MÃ©todos

JPlag emite dos mÃ©tricas por par, `AVG` y `MAX`. El parser toma **siempre `AVG`**, la media de las dos similitudes direccionales, porque es la magnitud simÃ©trica comparable con la `similarity` de Dolos y con la media de los dos porcentajes de Moss. Usar `MAX` producirÃ­a cifras sistemÃ¡ticamente mÃ¡s altas y una comparaciÃ³n desigual entre herramientas.

---

## Parte 2 â€” Dolos

Dolos es la mÃ¡s incÃ³moda de instalar en Windows porque compila analizadores nativos. Prueba las vÃ­as en este orden y quÃ©date con la primera que funcione.

### VÃ­a A â€” npm

```powershell
node --version
npm install -g @dodona/dolos
dolos --version
```

Si la instalaciÃ³n falla con errores de `node-gyp`, faltan herramientas de compilaciÃ³n: instala **Visual Studio Build Tools** con la carga de trabajo Â«Desarrollo para escritorio con C++Â» y repite. Si tampoco asÃ­, pasa a la vÃ­a B.

### VÃ­a B â€” Docker

Instala Docker Desktop, y luego:

```powershell
docker run --rm -v "${PWD}:/dolos" ghcr.io/dodona-edu/dolos-cli --version
```

En esta vÃ­a, cada comando `dolos` se sustituye por ese `docker run` completo, y las rutas se escriben tal como las ve el contenedor (`/dolos/...`).

### Claves de lenguaje

La documentaciÃ³n de Dolos no publica los identificadores exactos del parÃ¡metro `-l`. AverÃ­gualos antes de ejecutar:

```powershell
dolos run --help
```

Busca en la ayuda los valores admitidos. Para C# suele ser `c-sharp` o `csharp`, y para Java, `java`. **Confirma cuÃ¡l acepta tu versiÃ³n y anÃ³talo**, porque debe constar en MÃ©todos.

### EjecuciÃ³n

```powershell
dolos run -f csv -l csharp -o out_dolos_cs baselines_work\cohorte\csharp\*\*.cs
dolos run -f csv -l java   -o out_dolos_java baselines_work\cohorte\java\*\*.java
```

Si tu versiÃ³n no admite `-o`, omÃ­telo: Dolos crearÃ¡ un directorio de salida en la carpeta actual. En cualquier caso, el archivo que interesa es **`pairs.csv`**:

```powershell
Get-ChildItem -Recurse -Filter pairs.csv | Select-Object FullName, Length
```

Un detalle importante: si PowerShell no expande el comodÃ­n `*\*.cs`, expÃ¡ndelo tÃº y pasa la lista:

```powershell
$archivos = Get-ChildItem baselines_work\cohorte\csharp\*\*.cs | ForEach-Object { $_.FullName }
dolos run -f csv -l csharp -o out_dolos_cs $archivos
```

---

## Parte 3 â€” Integrar las tres herramientas

Con las salidas de JPlag y Dolos ya generadas, y los HTML de Moss que ya tienes:

```powershell
python baselines.py parsear --pares baselines_work\pares.csv `
  --entrada moss:cohorte:moss_cs.html moss:cohorte:moss_java.html `
            jplag:cohorte:RUTA_DEL_CSV_DE_JPLAG_CS jplag:cohorte:RUTA_DEL_CSV_DE_JPLAG_JAVA `
            dolos:cohorte:out_dolos_cs\pairs.csv dolos:cohorte:out_dolos_java\pairs.csv `
  --out baselines_raw.csv --faltantes-cero

python baselines.py evaluar --in baselines_raw.csv --tol-identico 5
```

FÃ­jate en dos cosas de la salida del `parsear`: cuÃ¡ntas comparaciones leyÃ³ de cada archivo (si alguna da 0, el formato no se reconociÃ³) y cuÃ¡ntos pares quedaron sin comparaciÃ³n por herramienta. Ese segundo nÃºmero es un resultado en sÃ­ mismo: en Moss fueron 55 de 120.

---

## QuÃ© anotar mientras ejecutas

Cuatro datos por herramienta, que van directos a MÃ©todos: la **versiÃ³n exacta** (`java -jar jplag.jar --version`, `dolos --version`), la **clave de lenguaje** que aceptÃ³, la **fecha y hora** de ejecuciÃ³n, y el **equipo** donde corriÃ³. Sin eso la comparaciÃ³n no es citable.

---

## Advertencia que ya conocemos por Moss

Moss nunca devolviÃ³ 100 % para archivos idÃ©nticos byte a byte: su rango fue 79â€“99. Es muy probable que JPlag y Dolos presenten el mismo desfase, porque las tres miden cobertura de coincidencia y no una similitud calibrada donde idÃ©ntico equivalga a 100.

Por eso, cuando tengamos las tres, **la tabla principal del manuscrito debe construirse sobre el patrÃ³n por categorÃ­a y las distribuciones de similitud**, no sobre el porcentaje agregado de coincidencia â€” que, como comprobamos, varÃ­a 25 puntos segÃºn la tolerancia que se elija para la categorÃ­a idÃ©ntico. La comparaciÃ³n honesta es cualitativa en su estructura y cuantitativa en cada categorÃ­a, no un ranking global.
