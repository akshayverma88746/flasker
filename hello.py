from flask import Flask, render_template, flash # flash for flashing messages
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
# Create a flask object
app = Flask(__name__)
app.config['SECRET_KEY']="nothing"
# Create a form class
class NameForm(FlaskForm):
    name = StringField("Please enter your name", validators=[DataRequired()])   # Create a text field for input
    submit = SubmitField("Submit")
# Create a route 
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

    

