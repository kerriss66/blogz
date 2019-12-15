from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'jslkjflsjdlfj999'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

# @app.before_request
# def require_login():
    # allowed_routes =['login', 'signup']
    # print(session)

    # if request.endpoint not in allowed_routes and 'username' not in session:
    #     return redirect ('/login')

# @app.route('/signup', methods=['POST', 'GET'])
# def signup():
    # user_error = ''
    # pass_error = ''
    # reenter_error = ''

    # if request.method == 'POST':
    #     username = request.form['username']
        # if (' ' in username) or (not username) or (username.strip() == "") or (len(username) <= 2) or (len(username) >=21):
        #     user_error = "Please enter a username between 3 and 20 characters and no spaces."
        #     username = ''

    #     password = request.form['password']
        # if (' ' in password) or (not password) or (password.strip() == "") or (len(password) <= 2) or (len(password) >=21):
        #     pass_error = "Please enter a password between 3 and 20 characters and no spaces."

    #     verify = request.form['verify']
        # if (reenter != password):
            # reenter_error = "Please reenter your same password."

        # if not user_error and not pass_error and not reenter_error:
            # return redirect('/newpost?user=' + username)   
#        
#         return render_template('index.html', username=username, user_error=user_error, pass_error=pass_error, reenter_error=reenter_error)
   
    #     existing_user = User.query.filter_by(username=username).first()
    #     if not existing_user:
    #         new_user = User(username, password)
    #         db.session.add(new_user)
    #         db.session.commit()
    #         session['username']= username
    #         return redirect('/newpost')
    #       
    #     else:
    #         return '<h1> Duplicate User </h1>'
    # return render_template('signup.html')

        
        if not title_error and not body_error:
            new_post = Blog(title, body) 
            db.session.add(new_post)   
            db.session.commit()
            return render_template('/individual_blog.html', title=title, blog=new_post)
        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error, title=title, body=body)

    return render_template('newpost.html')




# @app.route('/login', methods=['POST','GET'])
# def login():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     user = User.query.filter_by(username=username).first()
        
        # if not user and not user.password == password:
        #     return redirect('/signup')

    #     if user and user.password == password:
    #         session['username'] = username
    #         flash("Logged in")
    #         return redirect('/newpost')
    #     else:
    #         flash("User password incorrect, or user does not exist", "error")
    #         return redirect('/login')

    # return render_template('login.html')


# @app.route('/')
# def index():
    # owner = User.query.filter_by(username=session['username']).first()

    # if request.method == 'POST':
    #     blog_title = request.form['blog']
    #     new_blog = Blog(blog_title, owner)
    #     db.session.add(new_blog)
    #     db.session.commit()

    # blogs = Blog.query.filter_by(owner=owner).all()
    # return render_template('blog.html', blogs=blogs)

# @app.route('/logout')
# def logout():
    # del session['username']
    # return redirect('/')

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
