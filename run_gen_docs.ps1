
Write-Host "Generating docs/..."
Remove-Item -Recurse docs/*
pdm run pdoc src -o docs --math --mermaid -d restructuredtext --logo ../data/icon.ico --favicon ../data/icon.ico

Write-Host "Generating uml/..."
pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/

Write-Host "Generating dependency graphs in uml/..."
pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png