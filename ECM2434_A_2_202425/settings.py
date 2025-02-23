import os
from pathlib import Path

AUTH_USER_MODEL = "bingo.User"
WSGI_APPLICATION = 'ECM2434_A_2_202425.wsgi.application'

# 1️⃣ Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 2️⃣ Security Settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key')
DEBUG = True  # Change to False in production

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
TIME_ZONE = 'Europe/London'

# 3️⃣ Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Your Django apps
    'bingo',
]

# 4️⃣ Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Allow frontend requests
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5️⃣ CORS Settings (Allow Frontend to Access Backend)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# Allow all headers (e.g., Content-Type, Authorization)
CORS_ALLOW_HEADERS = [
    'Accept',
    'Content-Type',
    'Authorization',
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Allow requests from React
]
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type"]

# ✅ CSRF Settings for API requests
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]

# 6️⃣ Django REST Framework Config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
        'rest_framework.authentication.TokenAuthentication',  # If using token-based auth
        'rest_framework.authentication.SessionAuthentication',  # If using session-based auth
          # Use JWT tokens
    ),
}

# 7️⃣ Database Setup (Default: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# 8️⃣ Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'bingo.User' 

# 9️⃣ Static & Media Files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INTERNAL_IPS = [
    "127.0.0.1",
]

# 🔟 Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 1️⃣1️⃣ JWT Token Expiry
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'bingo', 'templates')],  # Add templates path
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

ROOT_URLCONF = 'ECM2434_A_2_202425.urls'
