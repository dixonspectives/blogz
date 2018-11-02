from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    blog_post = db.Column(db.Text, nullable=False)

def __init__(self, title, blog_post):
    self.title = title
    self.blog_post = blog_post

def blog_titles():
    return Blog.query.filter_by(title=False).all()

@app.route('/')
def redirect_to_main():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def index():
    blog_titles = db.session.query(Blog.title)
    dates = db.session.query(Blog.date)
    posts = db.session.query(Blog.blog_post)

    return render_template('blog-listing-form.html', title='Build a Blog', blog_titles=blog_titles, dates=dates, posts=posts)

if __name__ =='__main__':
    app.run()
