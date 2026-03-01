from celery.schedules import crontab
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path
import sys
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'jazzmin',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_extensions',
    'drf_spectacular',
    'phonenumber_field',
    'polymorphic',
]

LOCAL_APPS = [
   'users.apps.UsersConfig',
   'inventory',
   'notifications',
   'dashboard',
   'cart',
   'order',
   'wallet',
]


INSTALLED_APPS = [
    *EXTERNAL_APPS,
    *DJANGO_APPS,
    *LOCAL_APPS,
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


AUTH_USER_MODEL='users.BaseUserModel'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}



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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = "/static/"



REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],

    'DEFAULT_PAGINATION_CLASS': "config.pagination.CustomPagination",
    'PAGE_SIZE': 10,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


if 'test' in sys.argv:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv('REDIS'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }


REDIS_URL = os.getenv('REDIS')


CELERY_BROKER_URL = os.getenv("REDIS")
CELERY_RESULT_BACKEND = os.getenv("REDIS")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Cairo'


CELERY_BEAT_SCHEDULE = {
    "delete-old-notifications-every-day": {
        "task": "notifications.tasks.delete_old_message.delete_old_notifications",
        "schedule": crontab(hour=3, minute=0), 
    },
}

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN", "http://localhost:3000")

JAZZMIN_SETTINGS = {
    "site_title": "Ahmed Gaber",
    "site_header": "E-Commerce",
    "welcome_sign": "Hi",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commerce API',
    'DESCRIPTION': 'API documentation',
    'VERSION': '1.0.0',
}


STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
