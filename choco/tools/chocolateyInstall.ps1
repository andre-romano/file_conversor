$ErrorActionPreference = 'Stop'
$packageName = "file_conversor"
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"
$url = "https://github.com/andre-romano/file_conversor/releases/download/v1.0.0/file_conversor_win.zip"
$zipFile = Join-Path $toolsDir 'file_conversor_win.zip'

# Download the zip file
Get-ChocolateyWebFile -PackageName $packageName -FileFullPath $zipFile -Url $url

# Unzip to tools directory
Get-ChocolateyUnzip -FileFullPath $zipFile -Destination $toolsDir

# Remove the zip
Remove-Item -Force $zipFile

# Register executable with Chocolatey shim (not needed, due to $toolsDir destination)
# Install-BinFile -Name 'file_conversor' -Path $exePath

# Optionally make sure it's executable (relevant for some environments)
# Set-ItemProperty "$toolsDir\file_conversor.exe" -Name IsReadOnly -Value $false

# Note: Chocolatey automatically adds $toolsDir to PATH
