# run tests
./run_tests.ps1

# gen docs
./run_gen_docs.ps1

Write-Host "Building package..."
Remove-Item -Recurse build/*
Remove-Item -Recurse dist/*
pdm build

Write-Host "Building EXE..."
pdm run pyinstaller src/file_conversor.py --name file_conversor --onefile
