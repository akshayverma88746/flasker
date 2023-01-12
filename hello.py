from flask import Flask, render_template

# Create a flask object
app = Flask(__name__)

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