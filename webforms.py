from flask import Flask, render_template, flash, request, redirect, url_for# flash for flashing messages
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, email_validator, EqualTo, Length
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired()])
    password = StringField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    


# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])# Create a text field for input
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="PAssword must match")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    

# Create a form class
class NameForm(FlaskForm):
    name = StringField("Please enter your name", validators=[DataRequired()])   # Create a text field for input
    submit = SubmitField("Submit")
 


# Create password form
class PasswordForm(FlaskForm):
	email = StringField("What's Your Email", validators=[DataRequired()])
	password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
	submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Enter the title of the Post", validators=[DataRequired()])
    author = StringField("Enter Author Name")
    slug = StringField("Slug", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget= TextArea())
    submit = SubmitField("Submit")

