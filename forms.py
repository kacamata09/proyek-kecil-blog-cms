from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired

# buat form untuk tambah post
class TambahPost(FlaskForm):
    judul = StringField('Judul Postingan', validators=[DataRequired()])
    konten = TextAreaField('Konten')
    kategori = SelectField('Pilih Kategori', choices=('Berita', 'Viral', 'Teknologi'))

class Register(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    username = StringField('Nama Pengguna / Username', validators=[DataRequired()])
    password = PasswordField('Kata Sandi Anda', validators=[DataRequired()])
    password_konfirmasi = PasswordField('Masukkan Ulang Kata Sandi Anda', validators=[DataRequired()])
    