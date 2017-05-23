from pr.settings.base import *

SECRET_KEY = ''
DEBUG = False


ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'redmine',
        'USER': 'redmine',
        'PASSWORD': 'redminepass',
        'HOST': '129.74.246.37',
        'PORT': '5432'
    }
}

CAS_REDIRECT_URL = '/reports/home/'
CAS_IGNORE_REFERER = True
CAS_SERVER_URL = 'https://login.nd.edu/cas/login'
CAS_AUTO_CREATE_USERS = False


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

