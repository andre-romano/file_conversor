
import sys
from tasks_modules._config import *

# EXTERNAL DEPENDENCIES

CHOCO_DEPS = {
    "chocolatey-core.extension": "1.3.3",
    "ffmpeg": "",
    "ghostscript": "",
}

SCOOP_DEPS = {
    "ffmpeg": "",
    "ghostscript": "",
    "oxipng": "",
    "gifsicle": "",
    "mozjpeg": "",
}

# DOCKER
DOCKER_APT_DEPS = [
    "ffmpeg",
    "ghostscript",
    "libreoffice-nogui",
]
DOCKER_IMAGE_DEPS = {
    f"{DOCKER_REPOSITORY}/oxipng": "latest",
    f"{DOCKER_REPOSITORY}/mozjpeg": "latest",
    f"{DOCKER_REPOSITORY}/gifsicle": "latest",
}
DOCKER_PY_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
