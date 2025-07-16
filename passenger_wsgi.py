import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Load .env
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pluto.settings')

# Load WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
