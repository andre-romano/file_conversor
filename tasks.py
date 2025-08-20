# tasks.py (invoke)

from invoke.collection import Collection
from tasks_modules import base
from tasks_modules import choco
from tasks_modules import git
from tasks_modules import inno
from tasks_modules import locales
from tasks_modules import pyinstaller
from tasks_modules import pypi
from tasks_modules import scoop

# Create namespace collection
ns = Collection()
ns.add_collection(Collection.from_module(base), name="base")
ns.add_collection(Collection.from_module(choco), name="choco")
ns.add_collection(Collection.from_module(git), name="git")
ns.add_collection(Collection.from_module(inno), name="inno")
ns.add_collection(Collection.from_module(locales), name="locales")
ns.add_collection(Collection.from_module(pyinstaller), name="pyinstaller")
ns.add_collection(Collection.from_module(pypi), name="pypi")
ns.add_collection(Collection.from_module(scoop), name="scoop")
