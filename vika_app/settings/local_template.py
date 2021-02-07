from .base import *

SECRET_KEY = ""

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "../media")

STATICFILES_DIRS = (os.path.join(BASE_DIR, "../frontend/static"),)

STATIC_ROOT = os.path.join(BASE_DIR, "../static")

