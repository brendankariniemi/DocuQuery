from flask_caching import Cache

from config import DOCUQUERY_PDF

cache = Cache()


def init_caching(app):
    app.config['CACHE_TYPE'] = 'SimpleCache'
    cache.init_app(app)
    cache_data('uploaded_file', DOCUQUERY_PDF)


def cache_data(key, data, timeout=3600):
    cache.set(key, data, timeout=timeout)


def get_cached_data(key):
    return cache.get(key)
