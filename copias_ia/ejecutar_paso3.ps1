<#
ejecutar_paso3.ps1 — Ejecuta de principio a fin el Paso 3 de la revision M1:
genera las copias reescritas con IA, verifica que hacen lo mismo que el
original, las evalua con los cuatro modelos (en paralelo) y con JPlag/Dolos
(y Moss si esta disponible), y calcula los resultados.

Uso (PowerShell, desde C:\Repositorios\SimilCode\SimilCode-Benchmark):
    powershell -ExecutionPolicy Bypass -File copias_ia\ejecutar_paso3.ps1
Opciones:
    -Generadores "ollama:qwen2.5-coder:14b"     (por defecto)
    -Generadores "ollama:qwen2.5-coder:7b"      (equipos con poca memoria)
    -Generadores "openai:gpt-5.5-2026-04-23,anthropic:claude-opus-5"  (sin Ollama, via API)
    -SoloHasta generar | verificar | evaluar     (detenerse despues de ese paso)

Las claves de API se piden en pantalla sin mostrarse y viven solo en esta
sesion: nunca se escriben en disco ni en el registro.
Si el script se interrumpe, vuelva a ejecutarlo: retoma donde quedo.
#>
param(
    [string]$Generadores = "ollama:qwen2.5-coder:14b",
    [ValidateSet("", "generar", "verificar", "evaluar")][string]$SoloHasta = ""
)
$ErrorActionPreference = "Continue"   # los programas externos escriben en stderr; se revisa $LASTEXITCODE
$Repo = Split-Path -Parent $PSScriptRoot
Set-Location $Repo
$Log = Join-Path $PSScriptRoot "ejecucion_paso3.log"
Start-Transcript -Path $Log -Append | Out-Null

function Titulo($t) { Write-Host ""; Write-Host "==== $t ====" -ForegroundColor Cyan }
function Falla($t)  { Write-Host "ERROR: $t" -ForegroundColor Red; Stop-Transcript | Out-Null; exit 1 }
function Tiene($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

# ---------------------------------------------------------------- 1. Herramientas
Titulo "1. Comprobando herramientas"
foreach ($c in @("python", "dotnet", "javac", "java")) {
    if (-not (Tiene $c)) { Falla "Falta '$c'. Instalelo (ver README_COPIAS_IA.md) y vuelva a ejecutar." }
}
python -m pip install --quiet pandas numpy scipy
if ($Generadores -match "ollama:") {
    if (-not (Tiene "ollama")) { Falla "Falta Ollama (https://ollama.com) o use -Generadores con modelos por API." }
    foreach ($g in $Generadores.Split(",")) {
        if ($g -match "^ollama:(.+)$") {
            $m = $Matches[1]
            if (-not ((ollama list) -match [regex]::Escape($m))) { Write-Host "Descargando $m ..."; ollama pull $m }
        }
    }
}

# ---------------------------------------------------------------- 2. Claves
Titulo "2. Claves de API (no se muestran ni se guardan)"
$Prov = @{ openai = "OPENAI_API_KEY"; anthropic = "ANTHROPIC_API_KEY"; gemini = "GEMINI_API_KEY"; deepseek = "DEEPSEEK_API_KEY" }
foreach ($p in $Prov.Keys) {
    $var = $Prov[$p]
    if (-not [Environment]::GetEnvironmentVariable($var, "Process")) {
        $s = Read-Host "Pegue la clave de $p ($var)" -AsSecureString
        $plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
        if (-not $plain) { Falla "No se ingreso la clave de $p." }
        [Environment]::SetEnvironmentVariable($var, $plain, "Process")
    }
}

# ---------------------------------------------------------------- 3. Generar
Titulo "3. Generando las 60 copias ($Generadores)"
python copias_ia/generar_copias_ia.py --generadores $Generadores
if ($LASTEXITCODE -ne 0) { Falla "La generacion fallo." }
if ($SoloHasta -eq "generar") { Stop-Transcript | Out-Null; exit 0 }

# ---------------------------------------------------------------- 4. Verificar (+ hasta 3 regeneraciones)
Titulo "4. Verificando equivalencia funcional"
python copias_ia/verificar_equivalencia.py
if ($LASTEXITCODE -ne 0) { Falla "La verificacion fallo (revise dotnet/javac)." }
for ($intento = 1; $intento -le 3; $intento++) {
    $fallan = Import-Csv copias_ia/equivalencia_resumen.csv |
        Where-Object { $_.equivalent -ne "1" -and $_.statuses -notmatch "revision_manual" } |
        ForEach-Object { $_.copy_id }
    if (-not $fallan) { break }
    $ids = ($fallan -join ",")
    Write-Host "Regenerando (intento $intento de 3): $ids" -ForegroundColor Yellow
    python copias_ia/generar_copias_ia.py --generadores $Generadores --solo $ids
    python copias_ia/verificar_equivalencia.py --solo $ids
}
$manual = Import-Csv copias_ia/equivalencia_resumen.csv | Where-Object { $_.statuses -match "revision_manual" -and $_.equivalent -ne "1" }
if ($manual) {
    Write-Host ""
    Write-Host "REVISION MANUAL necesaria (programas con salida aleatoria):" -ForegroundColor Yellow
    $manual | ForEach-Object { Write-Host "  $($_.copy_id)  frente a  $($_.reference_id)" }
    Write-Host "Compare el codigo; si es equivalente, ponga 1 en 'equivalent' y el motivo en 'nota' de copias_ia\equivalencia_resumen.csv,"
    Read-Host "y pulse Enter para continuar (o Enter directamente para excluirlas)"
}
if ($SoloHasta -eq "verificar") { Stop-Transcript | Out-Null; exit 0 }

# ---------------------------------------------------------------- 5. Casos
Titulo "5. Construyendo metadata_ia.csv"
python copias_ia/construir_casos_ia.py
if ($LASTEXITCODE -ne 0) { Falla "No se pudo construir metadata_ia.csv." }

# ---------------------------------------------------------------- 6. Evaluar con los 4 modelos en paralelo
Titulo "6. Evaluando con los cuatro modelos en paralelo (puede tardar 3-4 horas)"
$jobs = @()
foreach ($p in @("openai", "anthropic", "gemini", "deepseek")) {
    $jobs += Start-Job -Name $p -ArgumentList $Repo, $p -ScriptBlock {
        param($repo, $p)
        Set-Location $repo
        for ($ronda = 1; $ronda -le 3; $ronda++) {   # 2a y 3a ronda reintentan las llamadas con error
            python benchmark_replicas.py run --cases metadata_ia.csv --prompt prompt.txt --replicas 3 --only $p --out "copias_ia/res_$p.csv" 2>&1 | Out-Null
        }
    }
}
$total = (Import-Csv metadata_ia.csv).Count * 3
while ($jobs | Where-Object { $_.State -eq "Running" }) {
    $msg = foreach ($p in @("openai", "anthropic", "gemini", "deepseek")) {
        $f = "copias_ia/res_$p.csv"
        $ok = 0; if (Test-Path $f) { $ok = (Import-Csv $f | Where-Object { -not $_.error }).Count }
        "{0} {1}/{2}" -f $p, $ok, $total
    }
    Write-Host ("[{0}] {1}" -f (Get-Date -Format HH:mm), ($msg -join " | "))
    Start-Sleep -Seconds 120
}
$jobs | Receive-Job | Out-Null
python -c "import pandas as pd; pd.concat([pd.read_csv(f'copias_ia/res_{p}.csv') for p in ['openai','anthropic','gemini','deepseek']]).to_csv('copias_ia/resultados_replicas_ia.csv', index=False); print('Unido: copias_ia/resultados_replicas_ia.csv')"
if ($SoloHasta -eq "evaluar") { Stop-Transcript | Out-Null; exit 0 }

# ---------------------------------------------------------------- 7. Detectores clasicos
Titulo "7. JPlag, Dolos y (si esta disponible) Moss"
python baselines.py preparar --metadata metadata_ia.csv --outdir baselines_work_ia
$entradas = @()
$jar = if (Test-Path ..\jplag.jar) { "..\jplag.jar" } elseif (Test-Path jplag.jar) { "jplag.jar" } else { "" }
if ($jar) {
    java -jar $jar baselines_work_ia\cohorte\csharp -l csharp -r out_jplag_cs_ia --csv-export *> copias_ia\jplag_cs_ia.log
    java -jar $jar baselines_work_ia\cohorte\java -l java -r out_jplag_java_ia --csv-export *> copias_ia\jplag_java_ia.log
    $entradas += "jplag:cohorte:out_jplag_cs_ia\results.csv", "jplag:cohorte:out_jplag_java_ia\results.csv"
} else { Write-Host "No se encontro jplag.jar; JPlag se omite." -ForegroundColor Yellow }
if (-not (Tiene "dolos") -and (Tiene "npm")) { npm install -g @dodona/dolos | Out-Null }
if (Tiene "dolos") {
    $cs = Get-ChildItem -Recurse baselines_work_ia\cohorte\csharp -Filter *.cs | ForEach-Object { $_.FullName }
    $jv = Get-ChildItem -Recurse baselines_work_ia\cohorte\java -Filter *.java | ForEach-Object { $_.FullName }
    dolos run -f csv -l csharp -o out_dolos_cs_ia $cs
    dolos run -f csv -l java -o out_dolos_java_ia $jv
    $entradas += "dolos:cohorte:out_dolos_cs_ia\pairs.csv", "dolos:cohorte:out_dolos_java_ia\pairs.csv"
} else { Write-Host "No se encontro dolos (npm install -g @dodona/dolos); Dolos se omite." -ForegroundColor Yellow }
if ((Test-Path .\moss) -and (Tiene "wsl")) {
    $wslRepo = (wsl wslpath -a ($Repo -replace '\\', '/')).Trim()
    wsl bash -c "cd '$wslRepo' && TRABAJO=baselines_work_ia/cohorte SUFIJO=_ia bash ejecutar_moss.sh"
    if (Test-Path moss_cs_ia.html) { $entradas += "moss:cohorte:moss_cs_ia.html", "moss:cohorte:moss_java_ia.html" }
} else { Write-Host "Moss se omite (falta el archivo 'moss' o WSL); se puede agregar despues." -ForegroundColor Yellow }
if ($entradas) {
    python baselines.py parsear --pares baselines_work_ia/pares.csv --entrada @entradas --out copias_ia/baselines_raw_ia.csv --faltantes-cero
}

# ---------------------------------------------------------------- 8. Analisis
Titulo "8. Resultados"
python copias_ia/analisis_copias_ia.py
Write-Host ""
Write-Host "Listo. Avise a Claude: los resultados estan en copias_ia\resultados_copias_ia.json" -ForegroundColor Green
Write-Host "Recuerde: NO suba a Git el archivo 'moss'. El registro de esta ejecucion esta en $Log"
Stop-Transcript | Out-Null
