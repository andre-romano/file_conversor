
## Build locales files (manually, if needed)
# invoke locales-build

Write-Host "Running GUI ..."
pdm run python src/file_conversor/gui/__main__.py @args
