from tkinter.tix import Form
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField, Form
from wtforms.validators import DataRequired, EqualTo, Length

# buat form untuk tambah post
class TambahPost(Form):
    judul = StringField('Judul Postingan', validators=[DataRequired()])
    konten = TextAreaField('Konten')
    kategori = SelectField('Pilih Kategori', choices=('Berita', 'Viral', 'Teknologi'))

class Register(Form):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    username = StringField('Nama Pengguna / Username', validators=[DataRequired()])
    password = PasswordField('Kata Sandi Anda', validators=[DataRequired(), EqualTo('password_konfirmasi', message='Belum cocok bro passwordnya')])
    password_konfirmasi = PasswordField('Masukkan Ulang Kata Sandi Anda', validators=[DataRequired()])
    simpan = SubmitField('REGISTER')
    