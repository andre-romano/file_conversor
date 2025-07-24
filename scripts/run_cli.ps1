
## Build locales files (manually, if needed)
# invoke locales-build

Write-Host "Running CLI ..."
pdm run python src/file_conversor.py @args
