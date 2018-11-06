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
        #self.date = date
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
            return redirect('/blog?id={0}'.format(new_post.id))

        else:
            return render_template('add-new-blog-post-form.html', title_input=title_input, title_input_error=title_input_error, post_input=post_input, post_input_error=post_input_error,)

    return render_template('add-new-blog-post-form.html')

def blog_posts():
    blog_posts = db.session.query(Blog.id, Blog.title, Blog.date, Blog.blog_post).all()
    return blog_posts

@app.route('/blog')
def index():
    blog_post_id = request.args.get('id')
    
    if blog_post_id != None:
        return render_template('blog-post-form.html', blog_posts=blog_posts(), blog_post_id=blog_post_id)

    return render_template('blog-listing-form.html', title='Build a Blog', blog_posts=blog_posts())

@app.route('/blog-post')
def blog_post():

    blog_post_id = request.args.get('blog_post_id')

    return render_template('blog-post-form.html', blog_post_id=blog_post_id)

if __name__ =='__main__':
    app.run()
