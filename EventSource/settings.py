"""
Django settings for EventSource project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os  

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGIN_URL = '/Login'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Absolute path to the directory static files should be collected to.
if DEBUG:
    STATIC_ROOT = '/Users/jamesporcelli/proj/EventSource/content'
else:
    STATIC_ROOT = ''
   
STATIC_URL = '/static/'
 
# Additional locations of static files
STATICFILES_DIRS = (
                os.path.join(BASE_DIR, 'static'),
                )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+r@*h*+#v((!drf=j-l-l0l_!l=zth6$bu+gl+q8$%_k!gpc#v'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'Main',
    'Login',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
                               'django.core.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.static',
                               'django.contrib.messages.context_processors.messages',
                               )

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'Main/templates/'),
    os.path.join(BASE_DIR, 'Login/templates'),
    os.path.join(BASE_DIR, 'Register/templates'),
)

ROOT_URLCONF = 'EventSource.urls'

WSGI_APPLICATION = 'EventSource.wsgi.application'

DATABASES = {
    'default' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geo_django',
        'USER': 'postgres',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# **!__
# @todo: Implement extensive logging capabilities
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}