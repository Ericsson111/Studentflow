from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired 
from studentflow.models import User


class RegistrationForm(FlaskForm): # Let user input there username, email and password to make an account
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)]) # validators = username_max = 20
    email = StringField('Email',
                        validators=[DataRequired(), Email()]) # validators = email
    password = PasswordField('Password', validators=[DataRequired()]) # password = data required
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')]) # confirm password
    age = BooleanField('Age') # confirm user is 13 or older
    submit = SubmitField('Sign Up') # submit

    def validate_username(self, username): # input username
        user = User.query.filter_by(username=username.data).first() # user filter by username first
        if user:
            raise ValidationError('That username is taken. Please choose a different one.') # if user choose the username were same with others, show this message to user

    def validate_email(self, email): # input email
        user = User.query.filter_by(email=email.data).first() # user filter by email first
        if user: 
            raise ValidationError('That email is taken. Please choose a different one.') # if user choose the email were same with others, show this message to user

    def validate_about(self, about): # input email
        user = User.query.filter_by(about=about.data).first() # user filter by email first
        if user: 
            raise ValidationError('That bio is taken. Please choose a different one.')


class LoginForm(FlaskForm): # Let user input there email and password to login and access the main page
    email = StringField('Email',
                        validators=[DataRequired(), Email()]) # validators = input email, no max
    password = PasswordField('Password', validators=[DataRequired()]) # validators = input password, no max
    remember = BooleanField('Remember Me') # BooleanField = True of False
    submit = SubmitField('Login') # submit


class UpdateAccountForm(FlaskForm): # Let user input there username, email and upload picture
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)]) # username = 20(max)
    email = StringField('Email',
                        validators=[DataRequired(), Email()]) # user email validators
    about = StringField('About',
                           validators=[DataRequired(), Length(min=2, max=100)]) # update user bio
    location = StringField('Location',
                           validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=11)])
    birth = StringField('Birth',
                           validators=[DataRequired(), Length(min=2, max=10)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) # uers profile, file allowed jpg, png
    submit = SubmitField('Update') # submit

    def validate_username(self, username): # username
        if username.data != current_user.username: # if usernamedata != current username
            user = User.query.filter_by(username=username.data).first() # filter by username first
            if user: 
                raise ValidationError('That username is taken. Please choose a different one.') # if current username got taken, user have to choose another one

    def validate_email(self, email): # user email
        if email.data != current_user.email: # if user_email data != current user_email
            user = User.query.filter_by(email=email.data).first() # filter by email first
            if user:
                raise ValidationError('That email is taken. Please choose a different one.') # if current email got taken, user have to choose another one

class PostForm(FlaskForm): # Let user input there post title, post content
    title = StringField('Title', validators=[DataRequired()]) # title = validators = input form
    content = TextAreaField('Content', validators=[DataRequired()]) # content = validators = input form
    tag = StringField('Tag',
                      validators=[DataRequired(), Length(min=2, max=50)]) # tag = validators = input form, max is 25 charactors 
    submit = SubmitField('Post') # submit

class FeedbackForm(FlaskForm): # Let user input there post title, post content
    content = TextAreaField('Content', validators=[DataRequired()]) # content = validators = input form
    submit = SubmitField('Post') # submit

class ChatForm(FlaskForm): # Let user input there post title, post content
    content = TextAreaField('Content', validators=[DataRequired()]) # content = validators = input form
    submit = SubmitField('Post') # submit

class CommentForm(FlaskForm): # Let user input there post title, post content
    name = StringField('Name',
                      validators=[DataRequired(), Length(min=2, max=20)])
    content = TextAreaField('Content', validators=[DataRequired()]) # content = validators = input form
    submit = SubmitField('Post') # submit