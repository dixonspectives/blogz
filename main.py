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
    #date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    blog_post = db.Column(db.Text, nullable=False)

def __init__(self, title, blog_post):
    self.title = title
    self.blog_post = blog_post
    #self.date = date

# This checks if the blog post column is empty
def is_empty():
    is_empty = db.session.query(Blog).filter_by(blog_post=None).all()
    return is_empty
# Since I am supposed to start at /blog, I redirect here to make it easier to navigate to where I am supposed to be   
@app.route('/')
def redirect_to_main():
    return redirect('/blog')
# Checks to see if the blog posts are be entered in a desired format and puts the title and post into the database
@app.route('/add-post', methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':
        title_input = request.form.get('title-of-post')
        post_input = request.form.get('blog-post-body')

        title_input_error = ''
        post_input_error = ''

        if len(title_input) < 3:
            title_input_error = 'Please enter a longer title.'

        if len(post_input) < 10:
            post_input_error = 'Please enter a longer blog post.'

        if post_input == 'Enter text here...':
            post_input_error = 'Please enter something else for the blog post.'

        if not title_input_error and not post_input_error:

            new_post = Blog(title_input, post_input)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')

        else:
            return render_template('add-new-blog-post-form.html', title_input=title_input, title_input_error=title_input_error, post_input=post_input, post_input_error=post_input_error,)

    return render_template('add-new-blog-post-form.html')


@app.route('/blog', methods=['POST', 'GET'])
def index():
    blog_titles = db.session.query(Blog.title)
    dates = db.session.query(Blog.date)
    posts = db.session.query(Blog.blog_post)
    total_posts = is_empty()
    
    return render_template('blog-listing-form.html', title='Build a Blog', total_posts=total_posts, posts=posts, blog_titles=blog_titles, dates=dates)

if __name__ =='__main__':
    app.run()
