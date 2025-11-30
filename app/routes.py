from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Score
from app.forms import RegisterForm, LoginForm
from app.utils import get_weather_data, get_random_question, get_user_location_from_ip
from app.quiz_data import QUIZ_QUESTIONS

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    """Halaman beranda dengan widget cuaca"""
    weather_data = None
    city = request.args.get('city', '')
    
    # Kalau tidak ada city di query, coba auto-detect dari IP
    if not city:
        try:
            city = get_user_location_from_ip()
            # Auto-load weather untuk location yang terdeteksi
            weather_data = get_weather_data(city)
        except:
            # Kalau gagal, pakai Jakarta sebagai fallback
            city = 'Jakarta'
            weather_data = get_weather_data(city)
    else:
        # User input manual
        weather_data = get_weather_data(city)
        if weather_data is None:
            flash('Kota tidak ditemukan atau terjadi error. Coba cek nama kota atau API key.', 'error')
    
    return render_template('index.html', weather_data=weather_data, city=city)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Halaman registrasi"""
    # Kalau sudah login, redirect ke home
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Buat user baru
        user = User(
            login=form.login.data,
            nickname=form.nickname.data
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('routes.login'))
        except Exception as e:
            db.session.rollback()
            flash('Terjadi error saat registrasi. Coba lagi.', 'error')
    
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman login"""
    # Kalau sudah login, redirect ke home
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Selamat datang, {user.nickname}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.index'))
        else:
            flash('Login atau password salah!', 'error')
    
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('routes.index'))


@bp.route('/quiz')
@login_required
def quiz():
    """Halaman kuis"""
    # Ambil total skor user
    total_score = current_user.get_total_score()
    
    # Ambil pertanyaan random
    question_data = get_random_question()
    
    # Acak urutan opsi agar jawaban benar tidak selalu di posisi pertama
    import random
    options = question_data['options'].copy()
    correct_index = question_data['correct']
    correct_answer = options[correct_index]
    
    # Shuffle opsi
    random.shuffle(options)
    
    # Cari index baru untuk jawaban benar setelah di-shuffle
    new_correct_index = options.index(correct_answer)
    
    # Update question data dengan opsi yang sudah di-shuffle
    question_data['options'] = options
    question_data['correct'] = new_correct_index
    
    # Simpan pertanyaan di session untuk validasi nanti
    session['current_question'] = question_data
    
    return render_template('quiz.html', 
                         question=question_data, 
                         total_score=total_score)


@bp.route('/quiz/answer', methods=['POST'])
@login_required
def check_answer():
    """Cek jawaban kuis dan update skor"""
    data = request.get_json()
    selected_answer = data.get('answer')
    
    # Ambil pertanyaan dari session (yang sedang ditampilkan)
    question = session.get('current_question')
    
    # Kalau tidak ada di session, ambil random (fallback)
    if not question:
        question = get_random_question()
    
    # Hapus pertanyaan dari session setelah dicek
    session.pop('current_question', None)
    
    is_correct = int(selected_answer) == question['correct']
    score_to_add = 10 if is_correct else 0
    
    # Simpan skor ke database
    if is_correct:
        score = Score(user_id=current_user.id, score=score_to_add)
        db.session.add(score)
        db.session.commit()
    
    # Update total score
    new_total_score = current_user.get_total_score()
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': question['correct'],
        'score_added': score_to_add,
        'total_score': new_total_score
    })


@bp.route('/leaderboard')
@login_required
def leaderboard():
    """Halaman papan peringkat"""
    # Ambil semua user dengan total score mereka
    users = User.query.all()
    leaderboard_data = []
    
    for user in users:
        total_score = user.get_total_score()
        leaderboard_data.append({
            'nickname': user.nickname,
            'login': user.login,
            'total_score': total_score
        })
    
    # Sort berdasarkan total score (tertinggi dulu)
    leaderboard_data.sort(key=lambda x: x['total_score'], reverse=True)
    
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

