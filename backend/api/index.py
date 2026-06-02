import sys
import os

# Add the backend root directory to the python path so imports of 'app' work properly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()
