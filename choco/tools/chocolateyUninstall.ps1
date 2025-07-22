$packageName = 'file_conversor'
$softwareName = 'File Conversor*' # Name in Programs and Features
$silentArgs = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG /choco' # Silent uninstall flags (matches installer)

# Remove the software
[array]$key = Get-UninstallRegistryKey -SoftwareName $softwareName
if ($key.Count -eq 1) {
    $key | % {
        $file = $_.UninstallString -replace '"', ''
        Uninstall-ChocolateyPackage -PackageName $packageName `
            -FileType 'exe' `
            -SilentArgs $silentArgs `
            -File $file
    }
}
elseif ($key.Count -gt 1) {
    Write-Warning "Multiple matches found for $softwareName!"
    Write-Warning "To prevent accidental data loss, no uninstall will be attempted."
    Write-Warning "Please manually remove the software from Control Panel."
}
