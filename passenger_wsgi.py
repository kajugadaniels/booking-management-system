import os
import sys

# Add the project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'pluto.settings'

# Load the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
