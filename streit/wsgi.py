"""
WSGI config for streit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/streit/')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streit.settings")

application = get_wsgi_application()
