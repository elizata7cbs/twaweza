import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
import logging

logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

SECRET_KEY = 'django-insecure-b5prd^t6_@jdhb=n9d0yo4=!sy9_5qs@3!%%nu@tc((bv)5%!b'

DEBUG = True
inProd = False

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_yasg',
    'users',
    'students',
    'parents',
    'paymentmodes',
    'expenses',
    'suppliers',
    'notifications',
    'schools',
    'inquiries',
    'usergroup',
    'transactions',
    'mpesa',
    'supportstaffs',
    'fee'

]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    # 'SLIDING_TOKEN_USE_REFRESH_TOKEN': True,
    # 'SLIDING_TOKEN_IGNORE_REFRESH_TOKEN_ON_AUTH': False,
    # 'SLIDING_TOKEN_STRATEGY': 'rest_framework_simplejwt.authentication.SlidingTokenAuthentication',
    # 'SLIDING_TOKEN_REFRESH_STRATEGY': 'rest_framework_simplejwt.authentication.SlidingTokenRefreshAuthentication',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_INFO': {
        'description': 'Edu-pay Authorization',
        'version': '1.0',
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend'),
        ],
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
WSGI_APPLICATION = 'core.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uwezo_pay',
        'USER': 'root',
        'PASSWORD': "",
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
AUTH_USER_MODEL = 'users.CustomUser'
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
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_DIR = os.path.join(BASE_DIR, 'static')
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

STATICFILES_DIRS = [
    STATIC_DIR,
]

STATIC_URL = '/static/'
AUTH_USER_MODEL = 'users.CustomUser'
CORS_ALLOW_ALL_ORIGINS = True

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'encodetechologies@gmail.com'
EMAIL_HOST_PASSWORD = 'ocfcpirrmuqqajki'
DEFAULT_FROM_EMAIL = 'info@uwezopay.com'

CONSUMER_KEY = "nk16Y74eSbTaGQgc9WF8j6FigApqOMWr"
CONSUMER_SECRET = "40fD1vRXCq90XFaU"
BSS_SHORT_CODE = "174379"
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
ACCESS_TOKEN_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
INITIATE_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
CALL_BACK_URL = "https://3db4-102-210-244-74.ngrok-free.app/MpesaCallBackURL.php"

# SUPERUSER DATA
SUPERUSER_USERNAME = 'superuser'
SUPERUSER_PASSWORD = 'superuser'
SUPERUSER_EMAIL = 'titus.eddys@gmail.com'
SUPERUSER_FIRST_NAME = 'Superuser'
SUPERUSER_LAST_NAME = 'Edupay'
SUPERUSER_PHONE_NUMBER = '254711223344'

# SCHOOLS DATA
SCHOOL_NAME = 'Dummy School'
SCHOOL_CODE = 'DS001'
COUNTRY = 'Kenya'
COUNTRY_CODE = 'KE'
COUNTY = 'Nairobi'
SUB_COUNTY = 'Westlands'
CITY = 'Nairobi'
STREET_ADDRESS = '123 Fake Street'
POSTAL_CODE = '00100'

PHONE_NUMBER1 = '0712345678'
PHONE_NUMBER2 = '0722345678'
PHONE_NUMBER_COUNTRY_CODE = '254'
EMAIL_ADDRESS = 'dummy@school.com'
WEBSITE = 'http://www.dummyschool.com'
REGISTRATION_NUMBER = 'REG123456'
SCHOOL_TYPE = 'PRIMARY'
BOARDING_STATUS = 'DAY'
CURRENCY = 'KES'
