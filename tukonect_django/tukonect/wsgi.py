"""
WSGI config for tukonect project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tukonect.settings')

application = get_wsgi_application()
