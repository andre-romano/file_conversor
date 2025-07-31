# File Conversor
Python program to convert and compress audio/video/text/etc files to other formats

**Summary**:
- [File Conversor](#file-conversor)
  - [External dependencies](#external-dependencies)
  - [Installing](#installing)
    - [For Windows](#for-windows)
      - [Option 1. Chocolatey Package Manager](#option-1-chocolatey-package-manager)
      - [Option 2. Scoop Package Manager](#option-2-scoop-package-manager)
      - [Option 3. Portable EXE](#option-3-portable-exe)
    - [For Linux](#for-linux)
      - [Option 1. Portable Binary](#option-1-portable-binary)
  - [Usage](#usage)
    - [CLI - Command line interface](#cli---command-line-interface)
    - [GUI - Graphical user interface](#gui---graphical-user-interface)
  - [License and Copyright](#license-and-copyright)

## External dependencies

This project requires the following external dependencies to work properly:
- FFmpeg
- Ghostscript
- qpdf

The app will prompt for download of the external dependencies, if needed.

## Installing

### For Windows

#### Option 1. Chocolatey Package Manager

1. Open PowerShell with Admin priviledges and run:
  ```bash
  choco install file_conversor
  ```

#### Option 2. Scoop Package Manager

1. Open PowerShell (no admin priviledges needed) and run:
  ```bash
  scoop install file_conversor
  ```

#### Option 3. Portable EXE

1. Download the latest version of the app (check [Releases](https://github.com/andre-romano/file_conversor/releases/) pages)
2. Extract ZIP file


### For Linux

#### Option 1. Portable Binary

1. Download the latest version of the app (check [Releases](https://github.com/andre-romano/file_conversor/releases/) pages)
2. Extract ZIP file

## Usage

### CLI - Command line interface

```bash
file_conversor COMMANDS [OPTIONS]
```

For more information about the usage:
- Issue `--help` option in the program

### GUI - Graphical user interface

*TODO*

## License and Copyright

Copyright (C) [2025] Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [./LICENSE](./LICENSE) file).

