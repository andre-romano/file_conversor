# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## Unreleased

<small>[Compare with latest](https://github.com/andre-romano/file_conversor/compare/be0a5b8d08cfe742e966f0b1b5b4211c6fe0bd15...HEAD)</small>

### Added

- add manual execution and dry_run option for GitHub actions workflow ([6cece80](https://github.com/andre-romano/file_conversor/commit/6cece80e342ebb47557bd7dfde3f6f97eaa78598) by Andre).
- add pypdf (merge, split, extract, rotate, encrypt, decrypt commands) configured autopep8 to avoid line breaking ([ab303ec](https://github.com/andre-romano/file_conversor/commit/ab303eca788cbe12d4aa944097e0dc86e452a623) by Andre).
- add "audio_video info" implementation using ffprobe ([5ca57eb](https://github.com/andre-romano/file_conversor/commit/5ca57eb96f9c693fdff159d1071cbbfbf607a35d) by Andre).
- add babel translations in project add tasks.py (invoke) for build automation add setup.iss and setup_run.ps1 (for Inno Setup exe generation) add github homepage, twine and babel, locales/ and data/ folders in pyproject.toml add license disclaimer in README.md ([060f255](https://github.com/andre-romano/file_conversor/commit/060f255824b25cfe56b32e6da8e870c0ede4f27e) by Andre).
- add CLI api tests add icon.ico config pytest with -x --ff ([e2ae812](https://github.com/andre-romano/file_conversor/commit/e2ae812e680850cbe0b8af03e85e3a17f99f5962) by Andre).
- add docs gen tools (pydeps, pyreverse) ([d080fde](https://github.com/andre-romano/file_conversor/commit/d080fde6f0d9db8950e0d21a428f864dd5e4445b) by Andre).
- add pyinstaller, pdoc, rich, CLI with Typer add config file (json) add AUTHORS.md add build instructions in pyproject.toml add ps1 scripts for automation ([44e33bf](https://github.com/andre-romano/file_conversor/commit/44e33bf8446d27205cc48c2c94709154ef85766b) by Andre).
- add vscode settings; add pytest + coverage to pyproject.toml add folders src/ and tests/ to pyproject.toml add pytest tests/ files for backend_abstract , ffmpeg_backend , and File 100% coverage tests ([b5f7266](https://github.com/andre-romano/file_conversor/commit/b5f7266e40ab3ff40b46e134dbdd91c7f2b26557) by Andre).

### Fixed

- fix: add MANIFEST.in file ; fix non-python folders convention as .folder_name ; ([651715d](https://github.com/andre-romano/file_conversor/commit/651715d7acd034ef9330b21ec84609ec756eff56) by Andre).
- fix: fix python package structure, add importlib.resources ([a9c94a0](https://github.com/andre-romano/file_conversor/commit/a9c94a09afb1d1263de32218c18ee1b9f3b4aaac) by Andre).
- fix: git actions ci/cd pipeline ([34e4bbc](https://github.com/andre-romano/file_conversor/commit/34e4bbc221be32666ae748147a6798280efe74af) by Andre).
- fix: git actions ([2b756ec](https://github.com/andre-romano/file_conversor/commit/2b756ecafe76c70ce62fdccd19fa7e74f4724de7) by Andre).
- fix:git actions ([3acd3a0](https://github.com/andre-romano/file_conversor/commit/3acd3a0fd3af8c507e436cad43b91a3c2b39f983) by Andre).
- fix: changelog ([566a3ed](https://github.com/andre-romano/file_conversor/commit/566a3ed1a27f643046ce99f11eca66404b0fd264) by Andre).
- fix: gitactions ([7b8f2ca](https://github.com/andre-romano/file_conversor/commit/7b8f2caa5e4b5b3579b1821187d0b0cb2f08dcdd) by Andre).
- fix: choco nuspec structure fix: CHOCO_API env location in git actions improve: add AUTHORS.md, LICENSE, pyproject.toml to dist/ files ([86f45d9](https://github.com/andre-romano/file_conversor/commit/86f45d9094681bd8a948379584c80ecdc6714b12) by Andre).
- fix: modify choco config to allow for ctx menu auto install ([20adb32](https://github.com/andre-romano/file_conversor/commit/20adb32bb0ef0f6ed06c26a8b4355f14d9d1e625) by Andre).
- fix: mkdir paths before using them ([0f5f2cc](https://github.com/andre-romano/file_conversor/commit/0f5f2ccbda3e922fa0c3007944e37a8ea66d98c4) by Andre).
- fix: choco create files syntax ([b805b5a](https://github.com/andre-romano/file_conversor/commit/b805b5ada2343a5b2ff182a47839e481b0dbf4d4) by Andre).
- fix babel translations in command help for typer code refactor (separated subcommands config, audio_video) code refactor (separated CONFIG, STATE and LOCALE in separate files) ([8dcfdcc](https://github.com/andre-romano/file_conversor/commit/8dcfdccd91bfb073dadd739ad2b005e85d264650) by Andre).

### Changed

- CHANGELOG.md for 0.1.0 ([ad8c587](https://github.com/andre-romano/file_conversor/commit/ad8c58724ca28d413c8fbf15d62a1144c417968a) by Andre).

<!-- insertion marker -->
