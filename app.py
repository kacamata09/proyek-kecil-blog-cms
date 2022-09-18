import re
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import TambahPost
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'isi random string aja atau buat generator secret key sendiri'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dbku'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
dbku = SQLAlchemy(app)
migrasidbku = Migrate(app, dbku)

# ORM blog
class Blog(dbku.Model):
    idPost = dbku.Column(dbku.Integer, primary_key=True)
    judulPost = dbku.Column(dbku.String(50), nullable=False)
    kontenPost = dbku.Column(dbku.String(2000))
    kategoriPost = dbku.Column(dbku.String(50))
    tanggalPost = dbku.Column(dbku.DateTime, default=datetime.today())
    

# jika terjadi error
@app.errorhandler(404)
def tidak_ditemukan(e):
    return render_template('blog/pencariangagal.html'), 404



# app index / home
@app.route('/')
def index():
    
    return render_template('index.html', titlepage='Home')

# app untuk login, register
@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')

# app untuk blog
@app.route('/post/tambahpost/', methods=['POST', 'GET'])
def tambah_post():
    if request.method == 'POST':
        judul = request.form['judul']
        konten = request.form['konten']
        kategori = request.form['kategori']
        tambahPost = Blog(judulPost=judul, kontenPost=konten, kategoriPost = kategori)
        dbku.session.add(tambahPost)
        dbku.session.commit()
        return redirect(url_for('tambah_post'))
    
    semua_post = Blog.query.all()
    return render_template('blog/tambahpost.html', form=TambahPost(), titlepage='Tambah Post', semuapost=semua_post)

@app.route('/post/editpost/<int:id>/', methods=['GET', 'POST'])
def edit_post(id):
    getPost = Blog.query.get_or_404(id)
    if request.method == 'POST':
        getPost.judulPost = request.form['judul']
        getPost.kontenPost = request.form['konten']
        getPost.kategoriPost = request.form['kategori']
        dbku.session.commit()
        return redirect(url_for('tambah_post'))
    return render_template('blog/editpost.html', form=TambahPost(), post=getPost, titlepage='Edit Post')

@app.route('/post/hapuspost/<int:id>/')
def hapus_post(id):
    getPost = Blog.query.get_or_404(id)
    dbku.session.delete(getPost)
    dbku.session.commit()
    return redirect(url_for('tambah_post'))
    

# post blog
@app.route('/post/')
def semua_post():
    semua_post = Blog.query.all()
    return render_template('blog/allpost.html', semuapost = semua_post, titlepage='All Post')

@app.route('/post/<kategori>/')
def kategori_post(kategori):
    kategoripost = Blog.query.filter(Blog.kategoriPost.ilike(f'%{kategori}%') )
    return render_template('blog/pencarianpost.html', kategori = kategoripost, titlepage=f'Kategori Post {kategori}')

# ilike("%ganye%"
@app.route('/post/halkategori/')
def halaman_kategori():
    return render_template('blog/halamankategori.html', titlepage='Kategori')


@app.route('/post/<int:id>/')
def detail_post(id):
    getPost = Blog.query.get_or_404(id)
    return render_template('blog/detailpost.html', post=getPost, titlepage=getPost.judulPost)


if __name__ == '__main__':
    app.run(debug=True)
    