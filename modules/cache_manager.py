import json
import os
from config import CACHE_FILE

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    else:
        cache = {}
    return cache

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)
