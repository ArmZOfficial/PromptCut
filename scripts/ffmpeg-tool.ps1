# Run the vendored ffmpeg-skill with tools installed for this Windows user.
$ErrorActionPreference = 'Stop'

$toolArguments = @()
$toolName = 'doctor'
if ($args.Count -gt 0) {
    $toolName = $args[0]
    $toolArguments = @($args | Select-Object -Skip 1)
}
if ($toolName -notmatch '^[a-z][a-z0-9_-]*(\.py)?$') {
    throw 'Pass a tool name, for example doctor, probe, or caption.'
}

$scriptName = "$($toolName -replace '\.py$', '').py"
if ($toolName -in 'doctor', 'contract') {
    $scriptName = '_contract.py'
    $toolArguments = @($toolName) + $toolArguments
}
$toolDirectory = Join-Path (Split-Path -Parent $PSScriptRoot) '.agents/skills/ffmpeg-skill/scripts'
$toolPath = Join-Path $toolDirectory $scriptName
if (-not (Test-Path -LiteralPath $toolPath -PathType Leaf)) {
    throw "Tool not found in ffmpeg-skill: $toolName"
}

$originalPath = $env:Path
$originalModel = $env:FFMPEG_SKILL_ASR_MODEL
try {
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    $machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $env:Path = "$originalPath;$userPath;$machinePath"

    $whisperDirectory = Join-Path $env:LOCALAPPDATA 'AffiliateVideo/whisper'
    $whisperExe = Join-Path $whisperDirectory 'whisper-cli.exe'
    $whisperModel = Join-Path $whisperDirectory 'ggml-large-v3-turbo-q5_0.bin'
    if ((Test-Path -LiteralPath $whisperExe -PathType Leaf) -and
        (Test-Path -LiteralPath $whisperModel -PathType Leaf)) {
        $env:Path = "$whisperDirectory;$env:Path"
        if (-not $env:FFMPEG_SKILL_ASR_MODEL) { $env:FFMPEG_SKILL_ASR_MODEL = $whisperModel }
    }

    if (Get-Command py.exe -ErrorAction SilentlyContinue) {
        & py.exe -3 -B $toolPath @toolArguments
    } else {
        & python.exe -B $toolPath @toolArguments
    }
    $status = $LASTEXITCODE
} finally {
    $env:Path = $originalPath
    $env:FFMPEG_SKILL_ASR_MODEL = $originalModel
}
exit $status
