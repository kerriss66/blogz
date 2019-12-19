from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'jslkjflsjdlfj@#999'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
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


@app.before_request
def require_login():
    allowed_routes =['login', 'signup', 'blog', 'index']
    # print(session)

    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    user_error = ''
    pass_error = ''
    reenter_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        reenter = request.form['reenter']
        exist = User.query.filter_by(username=username).first()

        if (username == '') or (len(username) < 3) or (len(username) > 20) or (' ' in username):
            user_error = 'Please enter a username between 3 & 20 characters with no spaces.'

        if (password == '') or (len(password) < 3) or (len(password) > 20) or (' ' in password):
            pass_error = 'Please enter a password between 3 & 20 characters with no spaces.'
   
        if password != reenter or reenter == '':
            reenter_error = 'Passwords must match.'

        if exist:
            user_error = 'Duplicate User.'

        if (len(username) >= 3) and (len(password) >= 3) and (password == reenter) and not exist:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('signup.html',
            username=username,
            user_error=user_error,
            pass_error=pass_error,
            reenter_error=reenter_error
            )

    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    username = ''
    user_error = ''
    pass_error = ''

    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if (username == '') or (password == ''):
            user_error = 'Please enter your username and/or password. If you do not have an account, please signup for one.'
            return redirect ('/login')

        if user and password:
            session['username'] = username
            return redirect('/newpost')

        if not user:
            user_error = 'Please signup for an account.'
            return redirect('/signup')
        else:
            user_error='Your username or password was incorrect.'
            return render_template('login.html')

    return render_template('login.html')


@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    all_blogs = Blog.query.all()

    if blog_id:
        all_blogs = Blog.query.filter_by(id=blog_id).all()
    if user_id:
        all_blogs = Blog.query.filter_by(owner_id=user_id).all()

    return render_template('blog.html', blogs=all_blogs)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    title_error = ''
    body_error = ''
  
    if request.method == 'POST':    
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        
        if (not title):
            title_error = 'Please enter the title for your new blog post.'
            title = ''
        if (not body):
            body_error = 'Please enter your new blog post.'
            body = ''
        
        if not title_error and not body_error:
            new_post = Blog(title, body, owner) 
            db.session.add(new_post)   
            db.session.commit()
            page_id = new_post.id
            return redirect('/blog?id={0}'.format(page_id))
            # return render_template('/individual_blog.html', title=title, blog=new_post)
        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error, title=title, body=body)

    return render_template('newpost.html')
    
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
    
if __name__ == '__main__':
    app.run()