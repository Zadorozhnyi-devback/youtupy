import json
import os
from pathlib import Path


__all__ = 'CacherMixin',


class CacherMixin:
    def _add_path_in_cache(self, path: str) -> None:
        cache = self._get_cache()

        cache['download_path'] = path

        with open(self._cache_path, 'w') as file:  # noqa
            file.write(json.dumps(cache))

    def _get_cache(self) -> dict:
        cache = dict()

        path = Path(self._cache_path)
        if path.exists() and path.stat().st_size > 0:
            with open(self._cache_path) as file:  # noqa
                cache = json.load(file)

        return cache

    @property
    def _cache_path(self) -> str:
        cache_path = f'{self._entry_point_path}/cache.json'  # noqa
        if not os.path.exists(cache_path):
            Path(cache_path).touch(exist_ok=True)  # noqa

        return cache_path
