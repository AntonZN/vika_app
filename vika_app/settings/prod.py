from .base import *

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["*"]

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    BASE_DIR, "../vika_app/settings/service.json"
)

DEFAULT_FILE_STORAGE = os.environ["DEFAULT_FILE_STORAGE"]
STATICFILES_STORAGE = os.environ["STATICFILES_STORAGE"]

GS_PROJECT_ID = os.environ["GS_PROJECT_ID"]
GS_STATIC_BUCKET_NAME = os.environ["GS_STATIC_BUCKET_NAME"]
GS_MEDIA_BUCKET_NAME = os.environ["GS_MEDIA_BUCKET_NAME"]

STATIC_URL = "https://storage.googleapis.com/{}/".format(GS_STATIC_BUCKET_NAME)
STATIC_ROOT = "static/"

MEDIA_URL = "https://storage.googleapis.com/{}/".format(GS_MEDIA_BUCKET_NAME)
MEDIA_ROOT = "media/"

UPLOAD_ROOT = "media/uploads/"

DOWNLOAD_ROOT = os.path.join(BASE_DIR, "static/media/downloads")
DOWNLOAD_URL = STATIC_URL + "media/downloads"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "../frontend/static"),)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
    }
}

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": os.environ["FCM_SERVER_KEY"],
}