# run tests
./run_tests.ps1

# gen docs
./run_gen_docs.ps1

Write-Host "Building package..."
pdm build

Write-Host "Building EXE..."
pdm run pyinstaller src/__main__.py --name file-conversor --onefile
