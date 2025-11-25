"""
WSGI configuration file untuk PythonAnywhere
Point web app ke file ini di PythonAnywhere dashboard
"""

import sys
import os

# Tambahkan path project ke sys.path
path = '/home/yourusername/Python_Pro-Muhammad_Farid_Zaki'  # Ganti dengan path kamu
if path not in sys.path:
    sys.path.insert(0, path)

# Import aplikasi
from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()

