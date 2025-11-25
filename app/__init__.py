from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Inisialisasi database
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Factory function untuk membuat Flask app"""
    
    # Set template dan static folder ke root project
    # base_dir adalah direktori TINGKAT ATAS (misalnya, Python_Pro-Muhammad_Farid_Zaki/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    
    # 🔑 PERBAIKAN UNTUK LOAD_DOTENV:
    # Secara eksplisit beritahu load_dotenv() di mana menemukan file .env
    dotenv_path = os.path.join(base_dir, '.env')
    load_dotenv(dotenv_path) 
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Konfigurasi secret key dan database
    # Variabel sekarang harus dimuat dari file .env
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-ganti-ini-di-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quiz_app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inisialisasi extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'
    login_manager.login_message = 'Silakan login dulu untuk mengakses halaman ini'
    
    # Import models agar bisa di-detect oleh SQLAlchemy
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    # Buat tabel database kalau belum ada
    with app.app_context():
        db.create_all()
    
    return app