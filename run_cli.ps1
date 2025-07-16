
Write-Host "Running CLI..."
$pdmArgs = $args -join " "
pdm run python src/__main__.py $pdmArgs
