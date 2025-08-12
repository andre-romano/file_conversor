# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [v0.2.0](https://github.com/andre-romano/file_conversor/releases/tag/v0.2.0) - 2025-08-12

<small>[Compare with v0.1.1](https://github.com/andre-romano/file_conversor/compare/v0.1.1...v0.2.0)</small>

### Features

- add ms office suite convertion (xls, ppt, doc) ([d5e84fc](https://github.com/andre-romano/file_conversor/commit/d5e84fc7a2ef7a018b1c470deeabf71b2e657795) by Andre).
- add pywin32 to invoke MSOffice VBA interface; add docx support with Word/Writer; ([c2e01f2](https://github.com/andre-romano/file_conversor/commit/c2e01f2eee180abcbc603ddbbdba99a5dc964337) by Andre).
- add pdf => docx ([46fa0f5](https://github.com/andre-romano/file_conversor/commit/46fa0f5ac132934d30195de472ab7c131537c896) by Andre).
- allow user to change preffered language ([b3b13a7](https://github.com/andre-romano/file_conversor/commit/b3b13a72b1c3a524044289b4fe33682cfa364509) by Andre).
- add docx => pdf conversion ([9f0dc1e](https://github.com/andre-romano/file_conversor/commit/9f0dc1e9118eca32384bd73835961f271cdf4255) by Andre).

### Bug Fixes

- bug in converting alpha img => non-alpha (e.g., png => jpg) ([1665bc1](https://github.com/andre-romano/file_conversor/commit/1665bc122b1c98db74c2fb2de7672abf10958078) by Andre).
- win menu incorrect syntax ([53df78a](https://github.com/andre-romano/file_conversor/commit/53df78a3094ac0c9b2dee3560210f4398f6eccd4) by Andre).
- get_executable returning .py main script ([54e4fee](https://github.com/andre-romano/file_conversor/commit/54e4fee0dc624ab5e4f0787088f54c3c05e2252f) by Andre).
- inno setup build ([40bd1ea](https://github.com/andre-romano/file_conversor/commit/40bd1eaee55ef7e63c5d83cde51a4b8c6bfe5c8f) by Andre).
- entrypoint of run_cli.ps1 ([b55269b](https://github.com/andre-romano/file_conversor/commit/b55269b57a6efc0b101f5bfb7f13333fafe43800) by Andre).
- rotation left/rigth menus ([b9f2bb6](https://github.com/andre-romano/file_conversor/commit/b9f2bb6455acf05dfd2ca126465c977a95e5ada3) by Andre).
- LF ends for .py ([4ad6f8f](https://github.com/andre-romano/file_conversor/commit/4ad6f8fc6432462e4db42db5b532c7fcab821917) by Andre).
- readme ([cbc090a](https://github.com/andre-romano/file_conversor/commit/cbc090a6eb2ca82aeee83309d38c79ad6dac6873) by Andre).

## [v0.1.1](https://github.com/andre-romano/file_conversor/releases/tag/v0.1.1) - 2025-08-06

<small>[Compare with first commit](https://github.com/andre-romano/file_conversor/compare/be0a5b8d08cfe742e966f0b1b5b4211c6fe0bd15...v0.1.1)</small>

### Features

- no-progress added fix: STATE has default values for all main_callback flags ([557315c](https://github.com/andre-romano/file_conversor/commit/557315cc2a63ff0c644b108ae912cba4f33f9661) by Andre).
- add qpdf lossless light compression ([3c7195e](https://github.com/andre-romano/file_conversor/commit/3c7195eb8fe55b5632765732ead6881936ac4aa7) by Andre).
- logging into .log file implemented ([c85bc0f](https://github.com/andre-romano/file_conversor/commit/c85bc0fdd84eb78441dd181bae014c85e8291dfb) by Andre).
- add batch file processing ([933c663](https://github.com/andre-romano/file_conversor/commit/933c6633f84f8c5adde1a65ff8fd35d413779059) by Andre).
- add img2pdf to convert img -> pdf improve: removed duplicated validators, improved code reusability ([0a88668](https://github.com/andre-romano/file_conversor/commit/0a8866898baec2ff3950d92eebc5dcc9a515e45b) by Andre).
- add pillow for image processing ([f63b2e9](https://github.com/andre-romano/file_conversor/commit/f63b2e98070cff5eb59ea6212a40b85d8ca84eb9) by Andre).
- add qpdf backend (for pdf repair) fix: undefined progress bar finishing in 100% now todo: improve progress bar measurement in pdf backend ([8c5d4be](https://github.com/andre-romano/file_conversor/commit/8c5d4bef5c38bd19b2ea96274d70d1821211a6d9) by Andre).
- add crossplatform support for package managers to automatically install missing external dependencies (ffmpeg, etc) feat: add brew (pkg manager for Linux + MacOS) feat: add scoop (pkg manager for Windows) fix: separated app_cmd from main entrypoint fix: load PATH from winreg (avoid problems with installing dependencies and other apps w/o closing win terminal) ([0076b4b](https://github.com/andre-romano/file_conversor/commit/0076b4bbb27485f702fb4949d4ff7e7d2024a4d5) by Andre).
- add CI/CD with Git Actions fix: remove choco using .gitignore (build is done by CI/CD now) ([7e5d517](https://github.com/andre-romano/file_conversor/commit/7e5d517ad4bdfac1294cf7302dfb6fc5d8cb1e7c) by Andre).

### Bug Fixes

- add MANIFEST.in file ; fix non-python folders convention as .folder_name ; ([651715d](https://github.com/andre-romano/file_conversor/commit/651715d7acd034ef9330b21ec84609ec756eff56) by Andre).
- fix python package structure, add importlib.resources ([a9c94a0](https://github.com/andre-romano/file_conversor/commit/a9c94a09afb1d1263de32218c18ee1b9f3b4aaac) by Andre).
- git actions ci/cd pipeline ([34e4bbc](https://github.com/andre-romano/file_conversor/commit/34e4bbc221be32666ae748147a6798280efe74af) by Andre).
- git actions ([2b756ec](https://github.com/andre-romano/file_conversor/commit/2b756ecafe76c70ce62fdccd19fa7e74f4724de7) by Andre).
- changelog ([566a3ed](https://github.com/andre-romano/file_conversor/commit/566a3ed1a27f643046ce99f11eca66404b0fd264) by Andre).
- gitactions ([7b8f2ca](https://github.com/andre-romano/file_conversor/commit/7b8f2caa5e4b5b3579b1821187d0b0cb2f08dcdd) by Andre).
- choco nuspec structure fix: CHOCO_API env location in git actions improve: add AUTHORS.md, LICENSE, pyproject.toml to dist/ files ([86f45d9](https://github.com/andre-romano/file_conversor/commit/86f45d9094681bd8a948379584c80ecdc6714b12) by Andre).
- modify choco config to allow for ctx menu auto install ([20adb32](https://github.com/andre-romano/file_conversor/commit/20adb32bb0ef0f6ed06c26a8b4355f14d9d1e625) by Andre).
- mkdir paths before using them ([0f5f2cc](https://github.com/andre-romano/file_conversor/commit/0f5f2ccbda3e922fa0c3007944e37a8ea66d98c4) by Andre).
- choco create files syntax ([b805b5a](https://github.com/andre-romano/file_conversor/commit/b805b5ada2343a5b2ff182a47839e481b0dbf4d4) by Andre).

### Code Refactoring

- improved CLI command consistency (always use -o for output / only argument allowed is input files, others are passed as options) feat: allow output_file to be optional (for most commands) feat: windows context menu for commands fix: locale path => script_folder/locales fix: define script_folder and script_executable within State (as should be) ([214943f](https://github.com/andre-romano/file_conversor/commit/214943f9b428f95b7e9493e4b69fa8301f072694) by Andre).
- add PLATFORM_* for platform constants improve: get local Python bin from .venv if testing unfrozen app (.py) ([288c356](https://github.com/andre-romano/file_conversor/commit/288c356187a98f075d91b4edb3b433ea3af04ca4) by Andre).
- moved app STATE control to State class feat: add -h alias for --help ([e483a97](https://github.com/andre-romano/file_conversor/commit/e483a9760598f9dcff83d87cfcd497bf74b02c59) by Andre).
- split code of batch file processing into backend and cli ([c6b8d31](https://github.com/andre-romano/file_conversor/commit/c6b8d314fc339083c73c6150b9f991a750f69bb3) by Andre).

