# file_conversor
Python CLI to convert and compress audio/video/text/etc files to other formats

**Summary**:
- [file\_conversor](#file_conversor)
  - [Install dependencies](#install-dependencies)
  - [Run program](#run-program)
  - [Build and Install](#build-and-install)


## Install dependencies

```bash
pip install pdm
pdm install
```

## Run program

```bash
pdm run python src/__main__.py 
```

For more information about the usage, read the [docs/](docs/) folder or issue `--help` command in the program.

## Build and Install

```bash
# for Python Wheel (cross-platform)
pdm build
pip install dist/*.whl

# for Windows (build .EXE)
pdm run pyinstaller src/__main__.py --name file-conversor --onefile
./dist/*.exe
```

