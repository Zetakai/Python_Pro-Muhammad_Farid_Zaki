import os
import sys  

path = '/home/CocoanutX/Python_Pro-Muhammad_Farid_Zaki'
if path not in sys.path:
    sys.path.append(path)

try:
    from app import create_app

    application = create_app()

except Exception as e:
    print(f"Error during application setup: {e}", file=sys.stderr)
    raise