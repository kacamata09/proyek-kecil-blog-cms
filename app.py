from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import TambahPost
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'isi random string aja atau buat generator secret key sendiri'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dbku'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
dbku = SQLAlchemy(app)

# ORM blog
class Blog(dbku.Model):
    idPost = dbku.Column(dbku.Integer, primary_key=True)
    judulPost = dbku.Column(dbku.String(50), nullable=False)
    kontenPost = dbku.Column(dbku.String(2000))
    tanggalPost = dbku.Column(dbku.DateTime, default=datetime.today())
    

# jika terjadi error
@app.errorhandler(404)
def tidak_ditemukan():
    return render_template('pencariangagal.html')



# app index / home
@app.route('/')
def index():
    
    return render_template('index.html')

# app untuk login, register
@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')


# app untuk blog
@app.route('/tambahpost/', methods=['POST', 'GET'])
def tambah_post():
    if request.method == 'POST':
        judul = request.form['judul']
        konten = request.form['konten']
        tambahPost = Blog(judulPost=judul, kontenPost=konten)
        dbku.session.add(tambahPost)
        dbku.session.commit()
        return redirect(url_for('tambah_post'))
    return render_template('blog/tambah_post.html', form=TambahPost())

@app.route('/post/')
def semua_post():
    semua_post = Blog.query.all()
    return render_template('blog/allpost.html', semuapost = semua_post)

@app.route('/post/<kategori>/')
def kategori_post(kategori):
    semua_post = Blog.query.all()
    return render_template('blog/kategoripost.html', semuapost = semua_post)

@app.route('/post/<int:id>/')
def detail_post(id):
    try:
        getPost = Blog.query.get_or_404(id)
    except:
        return redirect(url_for('tidak_ditemukan'))
    return render_template('blog/detailpost.html', post=getPost)


if __name__ == '__main__':
    app.run(debug=True)
    