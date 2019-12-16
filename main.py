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
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

@app.before_request
def require_login():
    allowed_routes =['login', 'blog', 'index', 'signup']
    print(session)

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
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if (' ' in username) or (not username) or (username.strip() == '') or (len(username) <= 2) or (len(username) >=21):
            user_error = 'Please enter a username between 3 and 20 characters and no spaces.'
            username = ''
        if (' ' in password) or (not password) or (password.strip() == '') or (len(password) <= 2) or (len(password) >=21):
            pass_error = 'Please enter a password between 3 and 20 characters and no spaces.'
        if (reenter != password):
            reenter_error = 'Please reenter your same password.'
        if existing_user:
            user_error = 'Duplicate User'

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username']= username
            return redirect('/newpost')
        else:
            return render_template('signup.html', username=username, user_error=user_error, pass_error=pass_error, reenter_error=reenter_error)
            
    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            flash('Logged in')
            return redirect('/newpost')
        if not user and not check_pw_hash(password, user.pw_hash):
            flash('User password incorrect, or user does not exist', 'error')
            return redirect('/login')

    return render_template('login.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    all_blogs = Blog.query.order_by(Blog.id())

    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('individual_blog.html', title=blog.title, body=blog.body, user=blog.owner.username, user_id=blog.owner_id)
    if user_id:
        blogs = Blog.query.filter_by(owner_id=user_id).all()
    return render_template('user.html', blogs=blogs)
    return render_template('blog.html', all_blogs=all_blogs)

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

    # return render_template('newpost.html')
    
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
    
if __name__ == '__main__':
    app.run()