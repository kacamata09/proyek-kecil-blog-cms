from flask import Flask, request, render_template, url_for, redirect
from models import dbku, Blog
app = Flask(__name__)




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
        return 
    return render_template('blog/tambah_post.html')

@app.route('/post/')
def semua_post():
    return render_template('blog/postingan.html')

@app.route('/post/<kategori>/')
def kategori_post(kategori):
    return render_template('blog/kategori_post.html')

@app.route('/post/<int:id>/')
def detail_post(id):
    return render_template('blog/detail_post.html')


if __name__ == '__main__':
    app.run(debug=True)