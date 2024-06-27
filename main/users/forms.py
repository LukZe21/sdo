from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_admin.contrib.sqla import ModelView
from main.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    firstname = StringField('სახელი',
                           validators=[DataRequired()])
    lastname = StringField('გვარი',
                           validators=[DataRequired()])
    nickname = StringField('მეტსახელი (შეგიძლიათ გამოტოვოთ)',
                           validators=[DataRequired()])
    email = EmailField('Email',
                       validators=[DataRequired()])
    
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')
        

class UpdateAccountForm(FlaskForm):
    firstname = StringField('სახელი',
                           validators=[DataRequired()])
    lastname = StringField('გვარი',
                           validators=[DataRequired()])
    nickname = StringField('მეტსახელი (შეგიძლიათ გამოტოვოთ)',
                           validators=[DataRequired()])
    email = EmailField('Email',
                       validators=[DataRequired()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_nickname(self, nickname):
        if nickname.data != current_user.nickname:
            user = User.query.filter_by(nickname=nickname.data).first()
            if user:
                raise ValidationError("That nickname is taken. Please choose a different one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")



class UserForm(FlaskForm):
    firstname = StringField('სახელი',
                            validators=[DataRequired()])
    lastname = StringField('გვარი',
                           validators=[DataRequired()])
    nickname = StringField('მეტსახელი')
    email = EmailField('Email',
                       validators=[DataRequired()])
    rank = SelectField('Rank', choices=[('მოდერატორი', 'მოდერატორი'), ('ხელმძღვანელი', 'ხელმძღვანელი'), ('თანახელმძღვანელი', 'თანახელმძღვანელი'), ('წევრი', 'წევრი')],
                        validators=[DataRequired()])
    in_group = BooleanField("Is this person in a working group?")
    score = IntegerField('Personal Score')
    submit = SubmitField('Save')

class UserView(ModelView):
    form = UserForm
    def on_model_change(self, form, model, is_created):
        return super(UserView, self).on_model_change(form, model, is_created)