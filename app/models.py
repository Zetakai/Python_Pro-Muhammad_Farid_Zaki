from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """Model untuk user/pengguna"""
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relasi ke scores (one-to-many)
    scores = db.relationship('Score', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash password sebelum disimpan"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Cek apakah password yang diinput benar"""
        return check_password_hash(self.password_hash, password)
    
    def get_total_score(self):
        """Hitung total skor dari semua kuis yang pernah dikerjakan"""
        return sum(score.score for score in self.scores)
    
    def __repr__(self):
        return f'<User {self.login}>'


class Score(db.Model):
    """Model untuk menyimpan skor kuis"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Score {self.score} by User {self.user_id}>'

