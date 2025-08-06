# File Conversor
Python program to convert and compress audio/video/text/etc files to other formats

**Summary**:
- [File Conversor](#file-conversor)
  - [External dependencies](#external-dependencies)
  - [Installing](#installing)
    - [For Windows](#for-windows)
      - [Option 1. Chocolatey Package Manager](#option-1-chocolatey-package-manager)
      - [Option 2. Scoop Package Manager](#option-2-scoop-package-manager)
      - [Option 3. PyPi](#option-3-pypi)
      - [Option 4. Installer (EXE)](#option-4-installer-exe)
    - [For Linux / MacOS](#for-linux--macos)
      - [Option 1. Homebrew (brew)](#option-1-homebrew-brew)
      - [Option 2. PyPi](#option-2-pypi)
  - [Usage](#usage)
    - [CLI - Command line interface](#cli---command-line-interface)
    - [GUI - Graphical user interface](#gui---graphical-user-interface)
    - [Windows Context Menu (Windows OS only)](#windows-context-menu-windows-os-only)
  - [Acknowledgements](#acknowledgements)
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

#### Option 3. PyPi

```bash
pip install pipx
python -m pipx ensurepath
python -m pipx install file_conversor
```

#### Option 4. Installer (EXE)

1. Download the latest version of the app (check [Releases](https://github.com/andre-romano/file_conversor/releases/) pages)
2. Execute installer (.exe file)


### For Linux / MacOS

#### Option 1. Homebrew (brew)

```bash
brew install file_conversor
```

#### Option 2. PyPi

```bash
pip install pipx
python -m pipx ensurepath
python -m pipx install file_conversor
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

1. Open Powershell and execute command below
  ```bash
  file_conversor win install-menu
  ```
2. Right click a file in Windows Explorer
3. Choose an action from "File Conversor" menu

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

