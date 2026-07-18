import sys
import os

# Ensure the root directory is in sys.path so imports work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api_server import app
