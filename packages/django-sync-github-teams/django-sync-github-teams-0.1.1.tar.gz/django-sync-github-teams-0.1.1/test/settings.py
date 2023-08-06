# minimal Django settings to make tests load and run without warnings

INSTALLED_APPS = [
    "django_sync_github_teams",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
USE_TZ = False
SECRET_KEY = "******"
