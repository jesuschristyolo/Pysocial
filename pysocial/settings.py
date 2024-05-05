from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--gaq#4d+vkzz7=%brkv@gr!t_0oqhi6$=8$g&r!d-ql^63$t&q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'pysocial.ru']

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'social_network.apps.SocialNetworkConfig',
    'channels',
    'users.apps.UsersConfig',
    'friends.apps.FriendsConfig',
    'chat.apps.ChatsConfig',
    'ribbon.apps.RibbonConfig',
    'bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    'social_django',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# # Алиас по умолчанию
# CACHE_MIDDLEWARE_ALIAS = "default"
# # Количество секунд хранения в кэше
# CACHE_MIDDLEWARE_SECONDS = 10
# # префикс для различения ключей кэширования
# CACHE_MIDDLEWARE_KEY_PREFIX = 'pysocial'

ROOT_URLCONF = 'pysocial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'pysocial/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.user_object',
            ],
        },
    },
]

WSGI_APPLICATION = 'pysocial.wsgi.application'
ASGI_APPLICATION = 'chat.asgi.application'

"""
Настройка Channels с помощью Redis
"""
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

"""
Настройка кэширования
"""

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Адрес нашего сервера
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': 'pysocial_db',
        'USER': 'pysocial',
        'PASSWORD': 'qwer1234',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'users.authentication.EmailAuthBackend',
]

SOCIAL_AUTH_JSONFIELD_ENABLED = True

"""
Редирект после успешной авторизации в github
"""
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'users:user_profile'

SOCIAL_AUTH_GITHUB_KEY = '602fe5e2403a995e04a1'
SOCIAL_AUTH_GITHUB_SECRET = '5d4a0b1f108add4abb0695efadfd910958f89bc8'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_HOST_USER = "pysocial@yandex.ru"
EMAIL_HOST_PASSWORD = "aoctvjsphmrylgmj"
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'home'

# crispy_form
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# crispy_form - END

"""
Логирование
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'C:/Python Projects/django_social/py_logs.log',
        },
    },
    # логгеры которые будут логировать наши сообщения
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

#
# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.auth_allowed',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'users.pipeline.new_users_handler',
#     'social_core.pipeline.user.create_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
# )
