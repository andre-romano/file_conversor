$ErrorActionPreference = 'Stop'
$packageName = "file_conversor"
$exeName = "$packageName.exe"
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"
$url = "https://github.com/andre-romano/file_conversor/releases/download/v1.0.0/file_conversor_win.zip"
$zipFile = Join-Path $toolsDir 'file_conversor_win.zip'
$exePath = Join-Path $toolsDir $packageName $exeName

# Download the zip file
Get-ChocolateyWebFile -PackageName $packageName -FileFullPath $zipFile -Url $url

# Unzip to tools directory
Get-ChocolateyUnzip -FileFullPath $zipFile -Destination $toolsDir

# Remove the zip
Remove-Item -Force $zipFile

# Register executable with Chocolatey shim (not needed, due to $toolsDir destination)
Install-BinFile -Name 'file_conversor' -Path $exePath

