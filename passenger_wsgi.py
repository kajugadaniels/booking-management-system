import os
import sys

# Add the project root directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pluto.settings')

# Get the WSGI application for the Django project
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
