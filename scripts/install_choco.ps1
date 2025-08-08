if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Output "Skip 'choco' install. Found in PATH."
    exit 0
}

[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Error "'choco' not found in PATH"
    exit 1
}
