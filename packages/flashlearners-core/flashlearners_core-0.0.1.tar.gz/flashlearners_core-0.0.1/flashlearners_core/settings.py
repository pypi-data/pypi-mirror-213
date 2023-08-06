import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PACKAGE_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

AUTH_USER_MODEL = 'app.User'

SECRET_KEY = os.getenv("SECRET_KEY", "@#$#EKNEak5(^1%s38r*jc3!96)@(#$IURNIO=2-3ny^_x4(l05s")

INSTALLED_APPS = ['daphne']

CORE_APPS = [
    'storages',
    'flashlearners_core',
    'flashlearners_core.app',
]


def db(key):
    return os.getenv(key)


def get_env(key, default=None):
    return os.getenv(key, default)


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.sqlite3",
            'NAME': "test.db"
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': db("DB_ENGINE"),
            'NAME': db('DB_NAME'),
            'USER': db('DB_USER'),
            'PASSWORD': db('DB_PASSWORD'),
            'HOST': db('DB_HOST'),
            'PORT': db('DB_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


#######################
# LOCALIZATION CONFIG #
#######################
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


###############
# MAIL CONFIG #
###############
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(PACKAGE_DIR, 'emails')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'admin@liquify.digital'
EMAIL_HOST_PASSWORD = 'vscqwkljfchpkzln'
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', 'Flashlearners<admin@flashlearners.com>')
SERVER_EMAIL = 'Flashlearners<admin@flashlearners.com>'
EMAIL_PORT = 587
# Gmail SMTP port (TLS): 587
# Gmail SMTP port (SSL): 465
EMAIL_USE_TLS = True
EMAIL_SIGNATURE = 'The Flashlearners Team'
ADMINS = (
    ('Fola', 'phourxx0001@gmail.com'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#################
# LOGGER CONFIG #
#################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(asctime)s %(name)s: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'root': {
        'handlers': ['console', ],
        'level': 'DEBUG'
    },
    'loggers': {
        'django.request': {
            'handlers': [
                'console', 'mail_admins'
            ],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

CORS_ALLOW_ALL_ORIGINS = True

####################
# ONESIGNAL CONFIG #
####################
ONE_SIGNAL_APP_ID = get_env("ONE_SIGNAL_APP_ID")
ONE_SIGNAL_REST_API_KEY = get_env("ONE_SIGNAL_REST_API_KEY")
ONE_SIGNAL_USER_AUTH_KEY = get_env("ONE_SIGNAL_USER_AUTH_KEY")

################
# MEDIA CONFIG #
################
FILE_UPLOAD_STORAGE = get_env("FILE_UPLOAD_STORAGE", default="s3")  # gcloud | s3

MEDIA_ROOT_NAME = "media"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"

if FILE_UPLOAD_STORAGE == "s3":
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    # Using django-storages
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_AUTO_CREATE_BUCKET = True
    AWS_S3_ACCESS_KEY_ID = get_env("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = get_env("AWS_S3_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = get_env("AWS_STORAGE_BUCKET_NAME", "flashlearners-media-v1-3di3n")
    AWS_S3_REGION_NAME = get_env("AWS_S3_REGION_NAME")
    AWS_S3_SIGNATURE_VERSION = get_env("AWS_S3_SIGNATURE_VERSION", default="s3v4")

    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
    AWS_DEFAULT_ACL = get_env("AWS_DEFAULT_ACL", default="public-read")

    AWS_PRESIGNED_EXPIRY = int(get_env("AWS_PRESIGNED_EXPIRY", default='10'))  # seconds

if FILE_UPLOAD_STORAGE == "gcloud":
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = get_env("GS_BUCKET_NAME")
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_DEFAULT_ACL = "publicRead"

