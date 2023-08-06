import string
import subprocess
from functools import lru_cache
from pathlib import Path
import random
from typing import Union, Callable

from connectome.storage import Storage
from wcmatch import glob

from .hash import is_hash, to_hash, load_tree_hash, load_tree_key
from .utils import call_git, HashNotFoundError

PathLike = Union[str, Path]


class Repository:
    def __init__(self, root: Path, storage: Storage, cache):
        self.storage = storage
        self.root = root
        self.cache = cache

    @property
    def current_version(self):
        return self.latest_version()

    def latest_version(self, path: PathLike = '.'):
        path = Path(path)
        if not (self.root / path).exists() and not is_hash(path):
            path = to_hash(path)

        if not (self.root / path).exists():
            raise FileNotFoundError(path)

        return call_git(f'git log -n 1 --pretty=format:%H -- {path}', self.root)

    # TODO: cache this based on path parents
    def get_key(self, *parts: PathLike, version: str):
        key, _, inside = self._split(Path(*parts), self._get_hash, version)

        # `relative` is a hash by itself
        if inside is None:
            return key

        inside = str(inside)
        tree = self.storage.load(load_tree_hash, key)
        if inside not in tree:
            raise HashNotFoundError(inside)

        return tree[inside]

    # TODO: this method will be deprecated in future versions
    def pull(self, *parts: PathLike, version: str):
        return self.storage.get_path(self.get_key(*parts, version=version), name=Path(parts[-1]).name)

    def glob(self, *parts: PathLike, version: str):
        key, hash_path, pattern = self._split(Path(*parts), self._get_hash, version)

        assert pattern is not None
        tree = self.storage.load(load_tree_hash, key)

        files = set(tree)
        for file in tree:
            files.update(map(str, list(Path(file).parents)[:-1]))
        files = sorted(files)

        return [hash_path / file for file in glob.globfilter(files, pattern, flags=glob.GLOBSTAR)]

    def load_tree(self, path: PathLike, version: str):
        exists, key = self._get_hash(Path(path), version)
        if not exists:
            raise HashNotFoundError(path)

        return self.storage.load(load_tree_hash, key)

    def _get_hash(self, path: Path, version: str):
        if version == UNCOMMITTED:
            return self._get_uncomitted_hash(path)
        return self._get_committed_hash(path, version)

    def _get_uncomitted_hash(self, relative: Path):
        path = self.root / relative
        if not path.exists():
            return False, None

        return True, load_tree_key(path)

    @lru_cache(None)
    def _get_committed_hash(self, relative: Path, version: str):
        relative = str(relative)
        if not relative.startswith('./'):
            relative = f'./{relative}'

        try:
            key = call_git(f'git show {version}:{relative}', self.root)
            if key.startswith('tree:'):
                key = key[5:]
            return True, key
        except subprocess.CalledProcessError:
            return False, None

    @staticmethod
    def _split(path: Path, read: Callable, *args):
        # TODO: use bin-search?
        for parent in list(reversed(path.parents))[1:]:
            hash_path = to_hash(parent)
            exists, payload = read(hash_path, *args)
            if exists:
                # TODO: make sure it's a tree hash
                return payload, hash_path, path.relative_to(parent)

        hash_path = to_hash(path)
        exists, payload = read(hash_path, *args)
        if not exists:
            raise HashNotFoundError(path)

        # TODO: make sure it's not a tree hash
        return payload, hash_path, None


UNCOMMITTED = '<UNTRACKED_CHANGES:' + ''.join(random.choices(string.ascii_letters + string.digits, k=64)) + '>'
