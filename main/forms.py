from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, PasswordField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from main.models import User

class DiscountElementForm(FlaskForm):
    name = StringField("Name",
                       validators=[DataRequired(), Length(min=1, max=100)])
    condition = StringField("Condition",
                       validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField("Description",
                       validators=[DataRequired(), Length(min=25, max=2500)])
    categories = StringField("Categories (Seperate with this '•')",
                       validators=[DataRequired(), Length(min=2, max=100)])
    expiration_duration = DateTimeField("Expiration Date (თთ/დდ/წწ)", format="%m/%d/%Y",
                       validators=[DataRequired()])
    img = FileField("Image", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

    toggle = BooleanField('Send to users?')

    submit = SubmitField('Publish')


class eventElementForm(FlaskForm):
    name = StringField("Name",
                       validators=[DataRequired(), Length(min=1, max=100)])
    description = StringField("Description",
                       validators=[DataRequired(), Length(min=25, max=2500)])
    categories = StringField("Categories (Seperate with this '•')",
                       validators=[DataRequired(), Length(min=2, max=2500)])
    start_date = DateTimeField('Start Date (თთ/დდ/წწ სს:წწ)', format="%m/%d/%Y %H:%M", validators=[DataRequired()])
    end_date = DateTimeField('End Date (თთ/დდ/წწ სს:წწ)', format="%m/%d/%Y %H:%M", validators=[DataRequired()])
    event_hoster = StringField('Host',
                        validators=[DataRequired(), Length(min=1, max=100)])
    location = StringField('Location',
                        validators=[DataRequired(), Length(min=5, max=200)])
    img = FileField("Image",
                    validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    
    dropdown = SelectField('Choose Type', choices=[('1', 'საუნივერსიტეტო'), ('2', 'სპონსორი')],
                           validators=[DataRequired()])
    
    toggle = BooleanField('Send to users?')

    submit = SubmitField('Publish')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired()])
    
    email = EmailField('Email', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')


class emailForm(FlaskForm):
    email = EmailField('Email',
                       validators=[DataRequired()])
    submit = SubmitField('Subscribe')