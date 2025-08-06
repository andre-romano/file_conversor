# tasks.py (invoke)

from invoke.collection import Collection
from tasks_modules import base, choco, git, inno, pypi

# Create namespace collection
ns = Collection()
ns.add_collection(Collection.from_module(base), name="base")
ns.add_collection(Collection.from_module(choco), name="choco")
ns.add_collection(Collection.from_module(git), name="git")
ns.add_collection(Collection.from_module(inno), name="inno")
ns.add_collection(Collection.from_module(pypi), name="pypi")
