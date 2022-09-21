from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# import forms
from forms import TambahPost, Register


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
    
class Pengguna(dbku.Model):
    __tablename__ = 'flasklogin-pengguna'
    
    idPengguna = dbku.Column(dbku.Integer, primary_key=True)
    namaLengkap = dbku.Column(dbku.String(255), nullable=False)
    username = dbku.Column(dbku.String(50), nullable=False)
    password_hash = dbku.Column(dbku.String(255), default='sandi123')
    
    # fungsi untuk hashing dan cek password
    # fungsi password akan berubah menjadi properti atau variable kelas ini menggunakan decorator property
    # tapi dengan raise attributeerror maka atribut tidak akan bisa diakses untuk melihat password
    @property
    def password(self):
        raise AttributeError('Maaf tidak bisa melihat password hehe')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, 'sha256')
    
    # @password.getter
    def cek_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    

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
    return render_template('login/login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        sandi = request.form['password']
        sandi_konfirmasi = request.form['password_konfirmasi']
        sandi_hash = generate_password_hash(sandi, 'sha256')
        tambah_pengguna = Pengguna(namaLengkap=nama, username=username, password_hash=sandi_hash)
        dbku.session.add(tambah_pengguna)
        dbku.session.commit()
        return redirect(url_for('login'))
        
    return render_template('login/register.html', form=Register())

@app.route('/admin/hapuspengguna/<int:id>')
def hapus_user(id):
    return render_template('login/hapususer.html')

@app.route('/admin/editpengguna/<int:id>')
def edit_user(id):
    return render_template('login/edituser.html')

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
    return render_template('blog/pencarianpost.html', cari = kategoripost, titlepage=f'Kategori Post {kategori}')

# ilike("%ganye%"
@app.route('/post/halkategori/')
def halaman_kategori():
    return render_template('blog/halamankategori.html', titlepage='Kategori')

# @app.route('/post/cari/', methods=['GET', 'POST'])
@app.route('/post/cari/')
def cari_post():
    cari = request.args.get('cari')
    if cari:
        caripost = Blog.query.filter(Blog.judulPost.ilike(f'%{cari}%') )
        return render_template('blog/pencarianpost.html', cari = caripost, hasilCari = cari)
    
    return render_template('blog/pencariangagal.html')
    


@app.route('/post/<int:id>/')
def detail_post(id):
    getPost = Blog.query.get_or_404(id)
    return render_template('blog/detailpost.html', post=getPost, titlepage=getPost.judulPost)


if __name__ == '__main__':
    app.run(debug=True)
    