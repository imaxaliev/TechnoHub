"""
Django settings for ecommerce_site project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '!lm70mphjh2-k6g4moq#_(19hjc80_p9rci$nul$4ty)6+=e=c')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = [
    'https://fierce-caverns-46536.herokuapp.com/',
    '127.0.0.1',
    'localhost'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'compressor',
    'sorl.thumbnail',
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# compressor

COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (
    ('text/less', r'lessc {infile} {outfile}'),
)

COMPRESS_OFFLINE = True

COMPRESS_ROOT = 'static'

# media

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')

MEDIA_URL = '/uploads/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_tb'
    }
}

TEMPLATE_DEBUG = os.environ.get('DJANGO_TEMPLATE_DEBUG', '') != 'False'

THUMBNAIL_PRESERVE_FORMAT = True

# stripe

STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_51HCr4JEQlCWbZ5K2vbMGOLpg84sG9z0BLYsHaxovbD3q8SchZvG3h2Xsh8YrZ9o2m5U6MTDepW8OSa9pp5ezQ5pV00MIqSIlvA')

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51HCr4JEQlCWbZ5K2cgvJlJcq3gnklL86HFcwz3CeLicvEjhuOFlYOEcCyGlrcal5wXCc9iafZ58zLSM2izfiaxgs00kYQ5hzHj')

DOMAIN_URL = 'http://127.0.0.1:8000/store/'

# auth

LOGIN_REDIRECT_URL = '/store/'

LOGOUT_REDIRECT_URL = '/account/login/'

CORS_ORIGIN_ALLOW_ALL = True

# Qiwi api

QIWI_PUBLIC_KEY = os.environ.get('DJ_QIWI_PUBLIC_KEY', '48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iP3ge5unWDK96rERUJQ4HVYVEKkFGFjxU6tpy6BBeexHRdmSmDFZNf6Bn27ePA9btnkdNdvQAhxt6r7kkYtrJFrJy89fE3qiP9rufYz8rH8')

QIWI_SECRET_KEY = os.environ.get('DJ_QIWI_SECRET_KEY', 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjBxem54ei0wMCIsInVzZXJfaWQiOiI3OTExODM3MzE1NCIsInNlY3JldCI6IjI3NTllMzUzNDEwYTQxMDQ3NjQ3YTA4Y2U3Njg0NjYzMzAyYzU0Y2ExZTYzMTc2YzAzZGFhMDE0ODFmNzQ2ZTQifX0=')

# modules

if DEBUG:
    import mimetypes
    mimetypes.add_type('application/javascript', '.js')


# db

import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

import django_heroku
django_heroku.settings(locals())
