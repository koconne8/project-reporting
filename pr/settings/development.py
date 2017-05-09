from pr.settings.base import *

DEBUG = True
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