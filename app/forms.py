from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    """Form untuk registrasi user baru"""
    login = StringField('Login', validators=[
        DataRequired(message='Login wajib diisi'),
        Length(min=3, max=20, message='Login harus 3-20 karakter')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password wajib diisi'),
        Length(min=4, message='Password minimal 4 karakter')
    ])
    
    confirm_password = PasswordField('Konfirmasi Password', validators=[
        DataRequired(message='Konfirmasi password wajib diisi'),
        EqualTo('password', message='Password tidak cocok')
    ])
    
    nickname = StringField('Nama Panggilan', validators=[
        DataRequired(message='Nama panggilan wajib diisi'),
        Length(min=2, max=50, message='Nama panggilan harus 2-50 karakter')
    ])
    
    submit = SubmitField('Daftar')
    
    def validate_login(self, login):
        """Cek apakah login sudah digunakan"""
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Login sudah digunakan, coba yang lain')
    
    def validate_nickname(self, nickname):
        """Cek apakah nickname sudah digunakan"""
        user = User.query.filter_by(nickname=nickname.data).first()
        if user:
            raise ValidationError('Nama panggilan sudah digunakan, coba yang lain')


class LoginForm(FlaskForm):
    """Form untuk login"""
    login = StringField('Login', validators=[
        DataRequired(message='Login wajib diisi')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password wajib diisi')
    ])
    
    submit = SubmitField('Masuk')

