param([switch]$CheckOnly)

$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$launcher = Join-Path $PSScriptRoot 'ffmpeg-tool.ps1'
$data = Join-Path $env:LOCALAPPDATA 'AffiliateVideo'
$whisper = Join-Path $data 'whisper'
$downloads = Join-Path $data 'downloads'
$modelName = 'ggml-large-v3-turbo-q5_0.bin'
$modelHash = '394221709CD5AD1F40C46E6031CA61BCE88931E6E088C188294C6D5A55FFA7E2'
$runtimeHash = 'B1514EBC099765E39FA37EB780B92A140A94C86BB0B3B3D98226B38825979732'
$installedFiles = @('whisper-cli.exe', 'whisper.dll', 'ggml.dll', 'ggml-base.dll', 'ggml-cpu.dll')

function Update-ToolPath {
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    $machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $env:Path = "$userPath;$machinePath;$env:Path"
}

function Test-Python {
    $probe = 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'
    if (Get-Command py.exe -ErrorAction SilentlyContinue) {
        & py.exe -3 -c $probe 2>$null
        return $LASTEXITCODE -eq 0
    }
    if (Get-Command python.exe -ErrorAction SilentlyContinue) {
        & python.exe -c $probe 2>$null
        return $LASTEXITCODE -eq 0
    }
    return $false
}

function Test-FFmpegTool([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { return $false }
    $firstLine = & $Name -version 2>$null | Select-Object -First 1
    if ($firstLine -notmatch 'version\s+(?:n)?(?<major>\d+)\.(?<minor>\d+)') { return $false }
    return ([version]"$($Matches.major).$($Matches.minor)") -ge [version]'6.1'
}

function Install-WingetPackage([string]$Package) {
    if (-not (Get-Command winget.exe -ErrorAction SilentlyContinue)) {
        throw 'WinGet is missing. Install Microsoft App Installer, then rerun this setup.'
    }
    & winget.exe install --id $Package --exact --scope user --source winget `
        --accept-package-agreements --accept-source-agreements --disable-interactivity
    Update-ToolPath
}

function Test-FileHashMatches([string]$Path, [string]$Hash) {
    return ((Test-Path -LiteralPath $Path -PathType Leaf) -and
        ((Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash -eq $Hash))
}

function Get-CheckedDownload([string]$Uri, [string]$Destination, [string]$Hash, [long]$ExpectedSize) {
    if (Test-FileHashMatches $Destination $Hash) { return }
    $partial = "$Destination.part"

    for ($attempt = 1; $attempt -le 4; $attempt++) {
        if (Test-Path -LiteralPath $partial) {
            if ((Get-Item -LiteralPath $partial).Length -ge $ExpectedSize) {
                if (-not (Test-FileHashMatches $partial $Hash)) { throw "Checksum mismatch: $partial" }
                Move-Item -LiteralPath $partial -Destination $Destination -Force
                return
            }
        }
        $downloadUri = $Uri
        if ($Uri -like 'https://huggingface.co/*') {
            $downloadUri += "?download=true&setup=$([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds())"
        }
        Write-Host "Downloading $(Split-Path -Leaf $Destination) ($attempt/4)"
        & curl.exe --ssl-revoke-best-effort --fail --location --show-error --connect-timeout 30 `
            --max-time 600 --continue-at - --output $partial $downloadUri
        if (Test-FileHashMatches $partial $Hash) {
            Move-Item -LiteralPath $partial -Destination $Destination -Force
            return
        }
    }
    throw "Download incomplete or invalid: $partial. Rerun to resume an incomplete file."
}

Update-ToolPath
if (-not $CheckOnly) {
    if (-not (Test-Python)) { Install-WingetPackage 'Python.Python.3.13' }
    if (-not (Test-FFmpegTool 'ffmpeg.exe') -or -not (Test-FFmpegTool 'ffprobe.exe')) {
        Install-WingetPackage 'Gyan.FFmpeg'
    }
}
if (-not (Test-Python)) { throw 'Python 3.10 or later must be available in this session.' }
if (-not (Test-FFmpegTool 'ffmpeg.exe') -or -not (Test-FFmpegTool 'ffprobe.exe')) {
    throw 'FFmpeg and FFprobe 6.1 or later must be available in this session.'
}

$runtimeMissing = @($installedFiles | Where-Object { -not (Test-Path -LiteralPath (Join-Path $whisper $_)) })
$model = Join-Path $whisper $modelName
if (-not $CheckOnly -and ($runtimeMissing.Count -gt 0 -or -not (Test-FileHashMatches $model $modelHash))) {
    New-Item -ItemType Directory -Force -Path $downloads, $whisper | Out-Null
    if ($runtimeMissing.Count -gt 0) {
        $archive = Join-Path $downloads 'whisper-cpp-v1.8.2-win-x64.zip'
        Get-CheckedDownload 'https://github.com/ggml-org/whisper.cpp/releases/download/v1.8.2/whisper-bin-x64.zip' `
            $archive $runtimeHash 3832432
        $extract = Join-Path $downloads 'whisper-cpp-v1.8.2-win-x64'
        Expand-Archive -LiteralPath $archive -DestinationPath $extract -Force
        foreach ($file in $installedFiles) {
            Copy-Item -LiteralPath (Join-Path $extract "Release/$file") -Destination $whisper -Force
        }
    }
    if (-not (Test-FileHashMatches $model $modelHash)) {
        $cachedModel = Join-Path $downloads $modelName
        Get-CheckedDownload "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$modelName" `
            $cachedModel $modelHash 574041195
        Move-Item -LiteralPath $cachedModel -Destination $model -Force
    }
}
if (-not (Test-FileHashMatches $model $modelHash)) { throw 'The verified local Thai ASR model is missing.' }

if (-not $CheckOnly) {
    foreach ($folder in @('Brief', 'Video', 'Insert', 'Output', '.work/tiktok_pro')) {
        New-Item -ItemType Directory -Force -Path (Join-Path $project $folder) | Out-Null
    }
}

$doctor = & $launcher doctor --json
if ($LASTEXITCODE -ne 0) { throw "ffmpeg-skill doctor failed. $doctor" }
$status = $doctor | ConvertFrom-Json
if (-not $status.ok -or $status.available -notcontains 'external:whisper') {
    throw 'FFmpeg or Whisper is missing a required tool. Run scripts/ffmpeg-tool.ps1 doctor for details.'
}
Write-Host "Ready: ffmpeg-skill $($status.version), FFmpeg $($status.ffmpeg), FFprobe $($status.ffprobe), local Whisper."
