
import sys
from tasks_modules._config import *

# EXTERNAL DEPENDENCIES

CHOCO_DEPS = {
    "chocolatey-core.extension": "1.3.3",
    "python": f"{PYTHON_VERSION}",
}

SCOOP_DEPS = {
    "python": f"{PYTHON_VERSION}",
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
