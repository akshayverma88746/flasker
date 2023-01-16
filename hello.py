from flask import Flask, render_template, flash, request # flash for flashing messages
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, email_validator
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
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

# Create Model of the database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable= False)
    email = db.Column(db.String(200), nullable = False, unique = True)
    favorite_color = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create String
    def __repr__(self):
        return '<Name %r>' %self.name

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])# Create a text field for input
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Color")
    submit = SubmitField("Submit")
    
# Create a form class
class NameForm(FlaskForm):
    name = StringField("Please enter your name", validators=[DataRequired()])   # Create a text field for input
    submit = SubmitField("Submit")
 
 #for updation


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name= form.name.data, email= form.email.data, favorite_color= form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("User Added Successfully")
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
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favorite_color = request.form['favorite_color']
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

