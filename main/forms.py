from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, PasswordField, EmailField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import os
from main import app
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


class DiscountElementView(ModelView):
    form = DiscountElementForm
    
    def on_model_change(self, form, model, is_created):
        if form.img.data:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], form.img.data.filename)
            form.img.data.save(image_path)
            model.img = form.img.data.filename
        return super(DiscountElementView, self).on_model_change(form, model, is_created)

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

class EventElementView(ModelView):
    form = eventElementForm
    
    def on_model_change(self, form, model, is_created):
        if form.img.data:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], form.img.data.filename)
            form.img.data.save(image_path)
            model.img = form.img.data.filename
        return super(EventElementView, self).on_model_change(form, model, is_created)


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

class emailForm(FlaskForm):
    email = EmailField('Email',
                       validators=[DataRequired()])
    submit = SubmitField('Subscribe')

class LogsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/logs.html')
    
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
    

class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    category = SelectField('Category', choices=[
        ('მარკეტინგი', 'მარკეტინგი'), 
        ('არაფორმალური განათლება', 'არაფორმალური განათლება'), 
        ('სპორტი', 'სპორტი'), 
        ('ტექნოლოგიები და ინოვაციები', 'ტექნოლოგიები და ინოვაციები')
    ])
    leader_id = IntegerField('ლიდერის ID', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()], default=100)

class GroupView(ModelView):
    form = GroupForm
    form_extra_fields = {
        'members': TextAreaField('Members', description="შეიყვანე ჯგუფის წევრები მძიმეების(,) გამოყოფით.")
    }
    form_columns = ('name', 'description', 'category', 'members', 'score')

    def on_model_change(self, form, model, is_created):
        if 'members' in form.data:
            model.members_list = [member.strip() for member in form.members.data.split(',')]
        return super(GroupView, self).on_model_change(form, model, is_created)