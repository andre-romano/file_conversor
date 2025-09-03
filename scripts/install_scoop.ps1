if (Get-Command scoop -ErrorAction SilentlyContinue) {
    Write-Output "Skip 'scoop' install. Found in PATH."
    exit 0
}

Import-Module Microsoft.PowerShell.Security -ErrorAction Stop
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Write-Error "'scoop' not found in PATH"
    exit 1
}
