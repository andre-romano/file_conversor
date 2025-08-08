# File Conversor
Python program to convert and compress audio/video/text/etc files to other formats

**Summary**:
- [File Conversor](#file-conversor)
  - [External dependencies](#external-dependencies)
  - [Installing](#installing)
    - [For Windows](#for-windows)
      - [Option 1. Scoop Package Manager (recommended)](#option-1-scoop-package-manager-recommended)
      - [Option 2. PyPi](#option-2-pypi)
      - [Option 3. Installer (EXE)](#option-3-installer-exe)
    - [For Linux / MacOS](#for-linux--macos)
      - [Option 1. PyPi](#option-1-pypi)
  - [Usage](#usage)
    - [CLI - Command line interface](#cli---command-line-interface)
    - [GUI - Graphical user interface](#gui---graphical-user-interface)
    - [Windows Context Menu (Windows OS only)](#windows-context-menu-windows-os-only)
  - [Acknowledgements](#acknowledgements)
  - [License and Copyright](#license-and-copyright)

## External dependencies

This project requires the following external dependencies to work properly:
- Python 3
- FFmpeg
- Ghostscript
- qpdf

The app will prompt for download of the external dependencies, if needed.

## Installing

### For Windows

#### Option 1. Scoop Package Manager (recommended)

1. Open PowerShell (no admin priviledges needed) and run:

```bash
scoop bucket add file_conversor https://github.com/andre-romano/file_conversor
scoop install file_conversor -k
```

#### Option 2. PyPi

```bash
pip install file_conversor
```

#### Option 3. Installer (EXE)

1. Download the latest version of the app (check [Releases](https://github.com/andre-romano/file_conversor/releases/) pages)
2. Execute installer (.exe file)

### For Linux / MacOS

#### Option 1. PyPi

```bash
pip install file_conversor
```

## Usage

### CLI - Command line interface

```bash
file_conversor COMMANDS [OPTIONS]
```

For more information about the usage:
- Issue `-h` for help

### GUI - Graphical user interface

*TODO*

### Windows Context Menu (Windows OS only)

1. Right click a file in Windows Explorer
2. Choose an action from "File Conversor" menu

## Acknowledgements

- Icons:
  - [Freepik](https://www.flaticon.com/authors/freepik)
  - [atomicicon](https://www.flaticon.com/authors/atomicicon)
  - [swifticons](https://www.flaticon.com/authors/swifticons)
  - [iconir](https://www.flaticon.com/authors/iconir)
  - [iconjam](https://www.flaticon.com/authors/iconjam)

## License and Copyright

Copyright (C) [2025] Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [./LICENSE](./LICENSE) file).

