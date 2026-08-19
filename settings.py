"""
Django settings for ecommerce_project.
E-Commerce Shopping Platform - Free Python Full Stack Internship (PY-EC-001)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# SECURITY
# -------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-CHANGE-THIS-KEY-BEFORE-DEPLOYMENT-!@#$%^&*()'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third party
    'rest_framework',
    'widget_tweaks',

    # Local apps
    'accounts',
    'catalog',
    'cart',
    'orders',
    'payments',
    'wishlist',
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

ROOT_URLCONF = 'ecommerce_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_summary',
                'catalog.context_processors.category_menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------
# This project is built for MySQL 8.x. We use PyMySQL (pure-python
# driver) so it works even if the mysqlclient C-extension cannot be
# compiled on the student's machine.
#
# To switch to MySQL:
#   1. Create a database:  CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4;
#   2. Set the environment variables below (or edit the values directly).
#   3. Run: python manage.py migrate
#
# If DB_ENGINE=sqlite (or no MySQL env vars are set), the project
# automatically falls back to SQLite so it can be tried out instantly.

DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite')  # 'mysql' or 'sqlite'

if DB_ENGINE == 'mysql':
    import pymysql
    pymysql.install_as_MySQLdb()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'ecommerce_db'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'root'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -------------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# I18N
# -------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# STATIC & MEDIA
# -------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# AUTH
# -------------------------------------------------------------------
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'catalog:product_list'
LOGOUT_REDIRECT_URL = 'catalog:product_list'

# -------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

# -------------------------------------------------------------------
# PAYMENT GATEWAY (Razorpay) - Demo/Test keys
# -------------------------------------------------------------------
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_XXXXXXXXXXXXXX')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'YOUR_TEST_SECRET_HERE')

# -------------------------------------------------------------------
# MESSAGES
# -------------------------------------------------------------------
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
