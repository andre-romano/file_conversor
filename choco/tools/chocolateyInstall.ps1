$packageName = 'file_conversor'
$url = 'https://github.com/andre-romano/file_conversor/releases/download/your-software.exe'
$fileType = 'exe'
$silentArgs = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /LOG /choco' # Silent install flags

Install-ChocolateyPackage $packageName $fileType $silentArgs $url