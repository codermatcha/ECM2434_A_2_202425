"""
WSGI config for ECM2434_A_2_202425 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Set the base directory (important if running as a standalone WSGI app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ECM2434_A_2_202425.settings")

try:
    application = get_wsgi_application()
except Exception as e:
    # Print errors to stderr for debugging
    import logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)
    logger.error("WSGI application failed to initialize", exc_info=True)
    raise
