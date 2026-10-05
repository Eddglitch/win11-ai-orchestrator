# $env:DEV_HOME\Config\PowerShell\profile_loader.ps1
# MASTER PROFILE LOADER v4.2 - PULSE EDITION
$env:DEV_CONFIG_PS = "$env:DEV_HOME\Config\PowerShell"

# 1. FUNCIÓN REFRESH INDEPENDIENTE
function Global:refresh {
    Clear-Host
    Write-Host "`n♻️ Recargando ecosistema..." -ForegroundColor Green
    . "$env:DEV_HOME\Config\PowerShell\profile_loader.ps1"
}

# 2. CARGA DEL TEMA
$ThemePath = "$env:DEV_CONFIG_PS\themes\gemini_compact.ps1"
if (Test-Path $ThemePath) { . $ThemePath }

# 3. CARGA DE MÓDULOS
$modulePath = "$env:DEV_CONFIG_PS\modules"
Get-ChildItem -Path $modulePath -Include "*.ps1","*.psm1" -Recurse | ForEach-Object {
    if ($_.Extension -eq ".psm1") {
        Import-Module $_.FullName -Global -Force -ErrorAction SilentlyContinue -DisableNameChecking
    } else {
        . $_.FullName
    }
}

# 4. ALIAS MAESTROS
if (Get-Alias ghelp -ErrorAction SilentlyContinue) { Remove-Item Alias:ghelp }
New-Alias -Name ghelp -Value Get-GeminiHelp -Scope Global -Force

# 5. MOSTRAR BANNER
if (Get-Command Show-WelcomeBanner -ErrorAction SilentlyContinue) {
    Show-WelcomeBanner
}

# 6. INICIALIZACIONES (Conda, Starship e IoT Pulse)
$condaHook = "$env:CONDA_PATH\shell\condabin\conda-hook.ps1"
if (Test-Path $condaHook) { . $condaHook }
if (Get-Command starship -ErrorAction SilentlyContinue) {
    Invoke-Expression (&starship init powershell)
}
