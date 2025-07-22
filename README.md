# File Conversor
Python program to convert and compress audio/video/text/etc files to other formats

**Summary**:
- [File Conversor](#file-conversor)
  - [External dependencies](#external-dependencies)
  - [Installing](#installing)
    - [For Windows](#for-windows)
      - [Option 1. Chocolatey Package Manager](#option-1-chocolatey-package-manager)
      - [Option 2. Portable EXE](#option-2-portable-exe)
    - [For Linux](#for-linux)
      - [Option 1. Using ``pip``](#option-1-using-pip)
      - [Option 2. Building and installing .WHL](#option-2-building-and-installing-whl)
  - [Usage](#usage)
    - [CLI - Command line interface](#cli---command-line-interface)
    - [GUI - Graphical user interface](#gui---graphical-user-interface)
  - [License and Copyright](#license-and-copyright)

## External dependencies

This project requires the following external dependencies to work properly:
- FFmpeg
- Ghostscript

## Installing

### For Windows

#### Option 1. Chocolatey Package Manager

1. Open PowerShell with Admin priviledges and run:
  ```bash
  choco install file_conversor
  ```

#### Option 2. Portable EXE

1. Download the latest version of the app (check [Releases](https://github.com/andre-romano/file_conversor/releases/) pages)
2. Extract ZIP file


### For Linux

#### Option 1. Using ``pip`` 

1. Run the following commands:
```bash
pip install file_conversor
```

#### Option 2. Building and installing .WHL

1. Install `python` in your distro
2. Install external dependencies in your distro
3. Build and install `.whl` file
  ```bash
  pip install pdm invoke
  invoke install-deps
  invoke build-whl
  invoke install-whl
  ```

## Usage

### CLI - Command line interface

```bash
file_conversor COMMANDS [OPTIONS]
```

For more information about the usage:
- Issue `--help` command in the program
- Read the [docs/](docs/) folder

### GUI - Graphical user interface

*TODO*

## License and Copyright

Copyright (C) [2025] Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [./LICENSE](./LICENSE) file).

