from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'jslkjflsjdlfj999'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
@app.route('/blog')
def blog():
    
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('individual_blog.html', blog=blog)

    blogs = Blog.query.order_by('id').all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    title_error = ''
    body_error = ''
  
    if request.method == 'POST':    
        title = request.form['title']
        body = request.form['body']
        
        if (not title):
            title_error = "Please enter the title for your new blog post."
            title = ''
        if (not body):
            body_error = "Please enter your new blog post."
            body = ''
        
        if not title_error and not body_error:
            new_post = Blog(title, body) 
            db.session.add(new_post)   
            db.session.commit()
            return render_template('/individual_blog.html', title=title, blog=new_post)
        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error, title=title, body=body)

    return render_template('newpost.html')
    

if __name__ == '__main__':
    app.run()
