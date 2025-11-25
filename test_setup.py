#!/usr/bin/env python3
"""
Script untuk test apakah semua dependencies sudah terinstall
Jalankan: python3 test_setup.py
"""

import sys

print("🔍 Checking dependencies...\n")

required_packages = [
    'flask',
    'flask_sqlalchemy',
    'flask_login',
    'flask_wtf',
    'wtforms',
    'werkzeug',
    'requests'
]

missing_packages = []

for package in required_packages:
    try:
        if package == 'flask_sqlalchemy':
            __import__('flask_sqlalchemy')
        elif package == 'flask_login':
            __import__('flask_login')
        elif package == 'flask_wtf':
            __import__('flask_wtf')
        else:
            __import__(package)
        print(f"✅ {package} - OK")
    except ImportError:
        print(f"❌ {package} - MISSING")
        missing_packages.append(package)

print("\n" + "="*50)

if missing_packages:
    print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    print("\nInstall dengan command:")
    print(f"  pip install {' '.join(missing_packages)}")
    print("\natau:")
    print(f"  pip install -r requirements.txt")
    sys.exit(1)
else:
    print("\n✅ All dependencies installed!")
    print("\n🚀 Ready to run! Execute:")
    print("  python3 run.py")
    sys.exit(0)

