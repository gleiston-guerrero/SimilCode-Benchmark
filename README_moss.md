# Incorporar Moss al protocolo de comparación

Moss completa la triangulación con las tres líneas base establecidas del área. Se integra en el mismo protocolo que Dolos y JPlag, y sus resultados se evalúan con las mismas bandas.

## Antes de nada: el identificador es una credencial

El script `moss` que Stanford entrega a cada solicitante contiene una línea `$userid=` con un número asignado. Ese número autentica todas las consultas contra el servidor, y el propio encabezado del script pide expresamente no colocarlo en un lugar de acceso público. **Este documento no lo reproduce, y ningún archivo del repositorio debe reproducirlo.**

En consecuencia: **no subas el archivo `moss` al repositorio**. Añádelo a `.gitignore` en la misma línea de defensa que cualquier archivo que contenga credenciales. Quien obtenga ese identificador puede consumir la cuota del titular, y sus consultas quedarán asociadas a esa cuenta. Si el número llega a aparecer en cualquier sitio de acceso público —un repositorio, un archivo permanente, una captura de pantalla—, la única medida efectiva es solicitar otro a `moss-request@cs.stanford.edu`: retirarlo del lugar donde apareció no revierte la exposición.

Para obtener un identificador, se solicita a esa misma dirección siguiendo las instrucciones publicadas por Stanford.

## Instalación en Windows

El script advierte que funciona en Unix y en Windows bajo Cygwin, pero no necesariamente con otras instalaciones de Perl. La vía más limpia y fiable es **WSL** (Subsistema de Windows para Linux):

```powershell
wsl --install -d Ubuntu
```

Dentro de Ubuntu, Perl ya viene instalado y el módulo `IO::Socket` es parte del núcleo, así que basta con guardar el script y darle permisos:

```bash
chmod u+x moss
./moss -h
```

Tu unidad `C:` es accesible desde WSL en `/mnt/c/`, de modo que puedes trabajar directamente sobre el repositorio sin copiar nada.

## Ejecución en modo cohorte

El guion `ejecutar_moss.sh`, versionado en este repositorio, automatiza lo que sigue con los parámetros exactos del estudio y se detiene con un mensaje explicativo si el cliente no está presente, si no lleva un identificador válido o si alguien lo ha versionado por error. Los comandos se documentan igualmente aquí para que el protocolo sea legible sin ejecutarlo.

```bash
bash ejecutar_moss.sh
```


Moss trae la opción `-d`, que trata **cada directorio como una entrega independiente** — exactamente la estructura que genera `baselines.py preparar`. Desde la raíz del repositorio, dentro de WSL:

```bash
cd /mnt/c/Repositorios/SimilCode/SimilCode-Benchmark

./moss -l csharp -d -n 1000 -c "SimilCode cohorte C#" baselines_work/cohorte/csharp/*/*.cs
./moss -l java   -d -n 1000 -c "SimilCode cohorte Java" baselines_work/cohorte/java/*/*.java
```

Cada corrida devuelve una URL con la página de resultados. Guárdala en disco:

```bash
curl -o moss_cs.html "PEGA_AQUI_LA_URL_DE_CSHARP"
curl -o moss_java.html "PEGA_AQUI_LA_URL_DE_JAVA"
```

Para el modo aislado se repite el mismo comando sobre cada carpeta de `baselines_work/aislado/`, aunque conviene advertir que son 120 consultas al servidor de Stanford: hazlo con pausas entre ellas y solo si el modo cohorte ya funcionó.

## Integrar los resultados

```powershell
python baselines.py parsear --pares baselines_work\pares.csv `
  --entrada moss:cohorte:moss_cs.html moss:cohorte:moss_java.html `
            dolos:cohorte:out_dolos_cs\pairs.csv jplag:cohorte:out_jplag_cs\results.csv `
  --out baselines_raw.csv --faltantes-cero

python baselines.py evaluar --in baselines_raw.csv --tol-identico 5
```

## Cuatro decisiones que deben constar en Métodos

**Moss emite dos porcentajes por par**, uno por cada entrega (qué proporción de ese archivo aparece en el otro). El parser toma la **media de ambos**, que es la magnitud simétrica comparable con la `similarity` de Dolos y la similitud media de JPlag. Es una elección, y como tal debe declararse.

**Moss solo lista las coincidencias por encima de su umbral interno.** Los pares que no aparecen en el informe se registran como similitud 0 mediante `--faltantes-cero`. Esto es una diferencia estructural frente a Dolos y JPlag, que emiten un valor para todos los pares, y debe reconocerse explícitamente: para Moss, «ausencia de reporte» y «similitud cero» no son exactamente lo mismo.

**El parámetro `-m`** controla cuántas veces puede aparecer un pasaje antes de ignorarlo; su valor por defecto es 10 y equivale al descuento de plantilla que hace Dolos. En este corpus, con quince grupos de referencia y cuatro variantes cada uno, ningún pasaje legítimo debería alcanzar ese umbral, así que el valor por defecto es apropiado. Documenta que se usó el valor por defecto y no se suministró archivo base (`-b`), en coherencia con las otras dos herramientas.

**El parámetro `-n 1000`** amplía el número de coincidencias mostradas por encima del valor por defecto de 250, necesario porque la cohorte genera muchos más pares que ese límite.

## Una nota para la sección de ética

Moss es un servicio remoto: la ejecución **sube el corpus a un servidor de Stanford**. En este caso no hay problema, porque los 120 pares fueron autorados para el estudio o extraídos del dominio público y ningún código estudiantil está implicado. Conviene decirlo en el manuscrito, y encaja de forma natural con la discusión sobre privacidad que el artículo ya desarrolla: la misma cautela que se exige al enrutar código por APIs comerciales aplica al enviarlo a un servicio académico de terceros.
