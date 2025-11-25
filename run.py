"""
File utama untuk menjalankan aplikasi Flask
Jalankan dengan: python run.py
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Untuk development, gunakan debug mode
    # Untuk production di PythonAnywhere, set debug=False
    app.run(debug=True, host='0.0.0.0', port=5000)

