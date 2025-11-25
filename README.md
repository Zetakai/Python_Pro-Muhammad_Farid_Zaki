# Kuis AI Python - Proyek Web dengan Flask

Aplikasi web kuis interaktif tentang Artificial Intelligence, Computer Vision, NLP, dan Python yang dibuat dengan Flask.

## Fitur

- **Halaman Beranda** dengan widget ramalan cuaca 3 hari (auto-detect lokasi user)
- **Sistem Registrasi & Login** dengan validasi login dan nickname unik
- **Kuis Interaktif** dengan 15+ pertanyaan random tanpa batas
- **Papan Peringkat** yang update otomatis setelah setiap kuis
- **UI Modern** dan responsive
- **Autentikasi User** dengan Flask-Login
- **Database** untuk menyimpan user dan skor

## Cara Menjalankan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

atau dengan pip3:

```bash
pip3 install -r requirements.txt --user
```

### 2. Setup Environment Variables

Buat file `.env` di root project dengan isi:

```
WEATHER_API_KEY=your_api_key_here
```

API key bisa didapatkan gratis di [OpenWeatherMap](https://openweathermap.org/api).

**Note:** Jika API key tidak di-set, aplikasi tetap bisa berjalan tapi fitur weather widget tidak akan berfungsi. Lokasi akan otomatis terdeteksi dari IP user, atau menggunakan Jakarta sebagai fallback.

### 3. Jalankan Aplikasi

```bash
python3 run.py
```

Aplikasi akan berjalan di `http://localhost:5000`

### 4. Test Dependencies

Untuk memastikan semua dependencies terinstall:

```bash
python3 test_setup.py
```

## Struktur Proyek

```
Python_Pro-Muhammad_Farid_Zaki/
├── app/
│   ├── __init__.py          # Factory function untuk Flask app
│   ├── models.py            # Database models (User, Score)
│   ├── routes.py            # Route handlers
│   ├── forms.py             # WTForms untuk validasi
│   ├── quiz_data.py         # Data pertanyaan kuis (15+ pertanyaan)
│   └── utils.py             # Utility functions (weather API, location detection)
├── templates/
│   ├── base.html            # Template dasar dengan navigation
│   ├── index.html           # Halaman beranda + weather widget
│   ├── register.html        # Halaman registrasi
│   ├── login.html           # Halaman login
│   ├── quiz.html            # Halaman kuis interaktif
│   └── leaderboard.html     # Papan peringkat
├── static/
│   ├── css/
│   │   └── style.css        # Styling modern & responsive
│   ├── js/
│   │   └── main.js          # JavaScript untuk flash messages
│   └── images/              # Folder untuk gambar/logo
├── .env                     # Environment variables (API keys)
├── .gitignore               # Git ignore rules
├── run.py                   # Entry point untuk development
├── cocoanutx_pythonanywhere_com_wsgi.py  # WSGI template (reference)
├── test_setup.py            # Script untuk test dependencies
├── requirements.txt         # Python dependencies
└── README.md                # Dokumentasi
```

## Fitur Detail

### Weather Widget
- Auto-detect lokasi user dari IP address
- Fallback ke Jakarta jika lokasi tidak terdeteksi
- Menampilkan ramalan cuaca 3 hari ke depan
- Menampilkan suhu siang dan malam hari
- Format tanggal dengan nama hari dalam Bahasa Indonesia

### Sistem Kuis
- 15+ pertanyaan tentang AI, Computer Vision, NLP, dan Python
- Pertanyaan diacak setiap kali
- Skor +10 untuk jawaban benar
- Total skor tersimpan di database
- Kuis bisa dimainkan tanpa batas

### Papan Peringkat
- Menampilkan semua user dengan total skor
- Diurutkan dari skor tertinggi
- Update otomatis setelah setiap kuis

## Deployment ke PythonAnywhere

### Setup Awal

1. **Clone dari GitHub** (recommended):
   ```bash
   cd ~
   git clone https://github.com/yourusername/your-repo.git Python_Pro-Muhammad_Farid_Zaki
   ```

2. **Install dependencies:**
   ```bash
   cd ~/Python_Pro-Muhammad_Farid_Zaki
   pip3.10 install --user -r requirements.txt
   ```

3. **Buat file `.env`:**
   ```bash
   nano .env
   # Isi: WEATHER_API_KEY=your_api_key_here
   ```

4. **Edit WSGI configuration** di Web tab (klik link WSGI configuration file):
   ```python
   import sys
   import os
   
   # Ganti 'yourusername' dengan username PythonAnywhere kamu
   path = '/home/yourusername/Python_Pro-Muhammad_Farid_Zaki'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   # Change working directory
   os.chdir(path)
   
   # Load environment variables
   from dotenv import load_dotenv
   load_dotenv(os.path.join(path, '.env'))
   
   # Import dan create aplikasi
   from app import create_app
   application = create_app()
   ```
   
   **Note:** File `cocoanutx_pythonanywhere_com_wsgi.py` di project bisa dijadikan referensi, tapi edit langsung di PythonAnywhere dashboard.

5. **Reload web app** di Web tab

### Update Project

```bash
cd ~/Python_Pro-Muhammad_Farid_Zaki
git pull origin main
# Reload web app di dashboard
```

## Catatan Penting

- Database SQLite (`quiz_app.db`) akan dibuat otomatis saat pertama kali run
- File `.env` sudah ada di `.gitignore` untuk keamanan
- Semua password di-hash menggunakan Werkzeug
- Kuis menggunakan pertanyaan random dari pool pertanyaan
- Lokasi user auto-detect dari IP, fallback ke Jakarta jika gagal

## Troubleshooting

### Error: "No module named flask"
Pastikan dependencies sudah terinstall: `pip3 install -r requirements.txt`

### Error: "Address already in use"
Port 5000 sudah digunakan. Edit `run.py` dan ganti port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Weather widget tidak muncul
- Pastikan API key sudah di-set di file `.env`
- Cek nama kota yang diinput (beberapa kota perlu nama dalam bahasa Inggris)

### Database error
Hapus file `quiz_app.db` dan restart aplikasi (database akan dibuat ulang)

## Developer

**Muhammad Farid Zaki**

---

Dibuat menggunakan Python & Flask
