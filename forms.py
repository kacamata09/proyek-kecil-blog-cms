from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

# buat form untuk tambah post
class TambahPost(FlaskForm):
    judul = StringField('Judul Postingan', validators=[DataRequired()])
    konten = TextAreaField('Konten')
