# File Conversor
Python program to convert and compress audio/video/text/etc files to other formats

**Summary**:
- [File Conversor](#file-conversor)
  - [Installing](#installing)
    - [For Windows](#for-windows)
      - [Option 1. Chocolatey Package Manager](#option-1-chocolatey-package-manager)
      - [Option 2. Setup file (.EXE)](#option-2-setup-file-exe)
    - [For Linux](#for-linux)
  - [External dependencies](#external-dependencies)
  - [Usage](#usage)
    - [CLI - Command line interface](#cli---command-line-interface)
    - [GUI - Graphical user interface](#gui---graphical-user-interface)
  - [License and Copyright](#license-and-copyright)

## Installing

### For Windows

#### Option 1. Chocolatey Package Manager

1. Open PowerShell with Admin priviledges and run:
  ```bash
  choco install file_conversor
  ```

#### Option 2. Setup file (.EXE)

1. Download the latest installer (check [Releases](https://github.com/andre-romano/file_conversor/releases/) pages)
2. Run the installer

**Attention:** External dependencies are installed automatically in Windows systems, during program installation. 
   - The installer will use [Chocolatey package manager](https://chocolatey.org/) to install those dependencies in Windows.

### For Linux

1. Install `python` in your distro
2. Install external dependencies in your distro
3. Build and install `.whl` file
  ```bash
  pip install pdm invoke
  pdm install
  pdm build
  pip install dist/*.whl
  ```


## External dependencies

This project requires the following external dependencies to work properly:
- FFmpeg
- Ghostscript

## Usage

### CLI - Command line interface

```bash
file_conversor COMMANDS [OPTIONS]
```

For more information about the usage:
- Issue `--help` command in the program
- Read the [docs/](docs/) folder

### GUI - Graphical user interface

**TODO**: build GUI

## License and Copyright

Copyright (C) [2025] Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [./LICENSE](./LICENSE) file).

