from flask_caching import Cache

cache = Cache()


def init_caching(app):
    app.config['CACHE_TYPE'] = 'SimpleCache'
    cache.init_app(app)
    # Removed default uploaded_file cache – no uploads in new workflow


def cache_data(key, data, timeout=3600):
    cache.set(key, data, timeout=timeout)


def get_cached_data(key):
    return cache.get(key)
