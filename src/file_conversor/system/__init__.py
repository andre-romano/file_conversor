# src\file_conversor\system\__init__.py

from file_conversor.system.abstract_system import *
from file_conversor.system.lin import *
from file_conversor.system.mac import *
from file_conversor.system.win import *


System: AbstractSystem
if AbstractSystem.Platform.get() == AbstractSystem.Platform.WINDOWS:
    System = WindowsSystem()
elif AbstractSystem.Platform.get() == AbstractSystem.Platform.MACOS:
    System = MacSystem()
elif AbstractSystem.Platform.get() == AbstractSystem.Platform.LINUX:
    System = LinuxSystem()
else:
    raise NotImplementedError(f"System platform {AbstractSystem.Platform.get()} is not supported.")
