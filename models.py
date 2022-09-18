from email.policy import default
from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
dbku = SQLAlchemy(app)

class Blog(dbku.Model):
    idPost = dbku.Column()
    judulPost = dbku.Column()
    kontenPost = dbku.Column()
    tanggalPost = dbku.Column(dbku.DateTime, default=datetime.today())
    