from PyInstaller.utils.hooks import collect_data_files  # pyright: ignore[reportMissingModuleSource]

# Collect all data files packaged inside ocrmypdf
datas = collect_data_files('ocrmypdf')

# Make sure the hidden import "ocrmypdf.data" is included
hiddenimports = [
    'ocrmypdf.data',
]
