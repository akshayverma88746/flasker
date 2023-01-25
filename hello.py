from flask import Flask, render_template, flash, request, redirect, url_for# flash for flashing messages
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, email_validator, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from webforms import UserForm, PostForm, NameForm, LoginForm, PasswordForm
# Create a flask object
app = Flask(__name__)
app.app_context().push()

# Add data base to our app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/our_users'

# Secret key
app.config['SECRET_KEY']="nothing"

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(300), nullable = False)
    content = db.Column(db.Text)
    #author = db.Column(db.String(300))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(300))
    # Create a forign key to connect to user and this will refer to the primary of the user
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Create Model of the database
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False, unique= True)
    name = db.Column(db.String(200), nullable= False)
    email = db.Column(db.String(200), nullable = False, unique = True)
    favorite_color = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Create some password stuff
    password_hash = db.Column(db.String(200)) #, nullable = False, unique = True)
    # Users can have many post
    post = db.relationship('Post', backref='poster')
    @property
    def password(self):
        raise AttributeError('Password is not a readle atribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Create String
    def __repr__(self):
        return '<Name %r>' %self.name



# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
    
    
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name= form.name.data, username=form.username.data, email= form.email.data, favorite_color= form.favorite_color.data, password_hash= hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash("Sign in successfull")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form = form, name = name, our_users= our_users)



@app.route('/')
def index():
    first_name = "Akshay"
    fav = ["Gaming", "travelling", "Gym", 41]
    return render_template('index.html', first = first_name, f = fav)
 

# Create user
@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)



#Create custom error page

# Invalid url
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
    


# Internal server error
@app.errorhandler(500)
def server(e):
    return render_template("500.html"), 500
    
# Function that return json
@app.route('/date')
def get_current_date():
    return {"Date": date.today()}
    
    
#Create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None;
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submission Successful")
    return render_template('name.html', name = name, form = form)



@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favorite_color = request.form['favorite_color']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update, id=id)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update,
				id=id)
	else:
		return render_template("update.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)



# Delete user
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None;
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully !!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form = form, name = name, our_users= our_users)
    except:
        flash("There was a problem deleting the user.... Try again")
        return render_template("add_user.html", form = form, name = name, our_users= our_users)
        

#Password test page 
@app.route('/test', methods=['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()
	# Validate Form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# Clear the form
		form.email.data = ''
		form.password_hash.data = ''

		# Lookup User By Email Address
		pw_to_check = Users.query.filter_by(email=email).first()
		
		# Check Hashed Password
		passed = check_password_hash(pw_to_check.password_hash, password)

	return render_template('test.html', email = email, password = password, pw_to_check = pw_to_check, passed = passed, form = form)


# Add post page 
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Post(title=form.title.data, poster_id=poster, content=form.content.data, slug=form.slug.data)
        form.title.data = ''
        form.content.data = '' 
        form.slug.data = ''
        
        db.session.add(post)    # For adding post 
        db.session.commit()     # For commiting changes
        flash("Post added successully")  
    
    return render_template('add_post.html', form=form)
    

# Show blog 
@app.route('/posts')
def posts():
    # getting all the post from the database
    posts = Post.query.order_by(Post.date_posted)
    return render_template("posts.html", posts=posts)
    

@app.route('/posts/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)
    
    
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Add to database
        db.session.add(post)
        db.session.commit()
        flash("Post updated successfully")
        return redirect(url_for('post', id=post.id))
    form.title.data=post.title 
    form.slug.data=post.slug
    form.content.data=post.content
    return render_template('edit_post.html', form=form)
    
    
@app.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post Deleted Successfully !!")
            posts = Post.query.order_by(Post.date_posted)
            return render_template("posts.html", posts=posts)
        except:
            flash("There was a problem deleting the Post.... Try again")
            posts = Post.query.order_by(Post.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash("Sorry you can't delete this post!!")
        posts = Post.query.order_by(Post.date_posted)
        return render_template("posts.html", posts=posts)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:   #user found check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password Please try again")
        else:
            flash("User does not exist")
    return render_template('login.html', form=form)
    
    
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update,
				id=id)
    else:
        return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)
    return render_template('dashboard.html')
    
    
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logout")
    return redirect(url_for('login'))
