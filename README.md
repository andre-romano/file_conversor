<!-- [![Patreon](https://img.shields.io/badge/Patreon-Support-orange?logo=patreon)](https://www.patreon.com/andre-romano) -->

# File Conversor
Python program to convert, compress and manipulate audio/video/text/docs/etc files to other formats.

**Summary**:
- [File Conversor](#file-conversor)
  - [Features](#features)
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
  - [Support this project](#support-this-project)
    - [Gold tier supporters](#gold-tier-supporters)
    - [Silver tier supporters](#silver-tier-supporters)
    - [Bronze tier supporters](#bronze-tier-supporters)
  - [Acknowledgements](#acknowledgements)
  - [License and Copyright](#license-and-copyright)

## Features
- Integration with Windows Explorer context menu (right click in file).
- Compress files (mp4, mp3, pdf, jpg, etc).
- Convert multiple file formats (xlsx <=> ods, docx => pdf, mkv <=> mp4, jpg <=> png, etc).
- Get metadata info about files (EXIF for images, stream data for video/audio, etc).
- Perform manipulations upon files (PDF split/rotation/encryption, image rotation/enhancements, etc).
- Batch file manipulation (using operation pipelines and config files, for task automation and advanced usage needs).
- CLI for script automation.

## External dependencies

This project requires the following external dependencies to work properly:
- Python 3
- LibreOffice (or Microsoft Office)
- FFmpeg
- Ghostscript

The app will prompt for download of the external dependencies, when needed.

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
  
<img src="./readme/ctx_menu.jpg" width="600px">

## Support this project

If you enjoy this project, consider supporting us with a donation in our Github Sponsors.

### Gold tier supporters

### Silver tier supporters

### Bronze tier supporters

## Acknowledgements

We would like to say our thanks to the incredible work provided by other contributors to this project:

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

