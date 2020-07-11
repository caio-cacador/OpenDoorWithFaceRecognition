from os import path


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
SOURCES = path.join(BASE_DIR, 'sources')
MEDIA_ROOT = path.join(BASE_DIR, 'faces')
