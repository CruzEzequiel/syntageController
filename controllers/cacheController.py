import time
import json
import os
from threading import Lock

class SimpleCache:
    def __init__(self, cache_file='cache.json'):
        self.cache_file = cache_file
        self.cache = {}
        self.lock = Lock()
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    current_time = time.time()
                    # Filtrar entradas expiradas
                    self.cache = {k: (v['value'], v['expiry']) for k, v in data.items() if current_time < v['expiry']}
            except (json.JSONDecodeError, KeyError):
                # Si hay error, empezar con cache vacío
                self.cache = {}

    def _save_cache(self):
        data = {k: {'value': v, 'expiry': e} for k, (v, e) in self.cache.items()}
        with open(self.cache_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get(self, key):
        with self.lock:
            if key in self.cache:
                data, expiry = self.cache[key]
                if time.time() < expiry:
                    return data
                else:
                    del self.cache[key]
            return None

    def set(self, key, value, ttl=300):  # ttl en segundos, default 5 minutos
        with self.lock:
            self.cache[key] = (value, time.time() + ttl)
            self._save_cache()

# Instancia global del cache
cache = SimpleCache()