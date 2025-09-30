$ErrorActionPreference = "Stop"

function Update-Env {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path, "Process")
}

Update-Env

if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Python is already installed."
    exit 0
}

IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (IsAdmin) {    
    if (Get-Process -Name "choco" -ErrorAction SilentlyContinue) {
        Write-Host "Chocolatey is already running. Please wait for it to finish."
        exit 1
    }

    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Host "Installing Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Update-Env
    }

    choco install python -y
}
else {
    if (Get-Process -Name "scoop" -ErrorAction SilentlyContinue) {
        Write-Host "Scoop is already running. Please wait for it to finish."
        exit 1
    }

    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
        Write-Host "Installing Scoop..."
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
        Update-Env
    }

    scoop install python
}

