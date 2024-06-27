from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, StringField, PasswordField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_admin import BaseView, expose


class emailForm(FlaskForm):
    email = EmailField('Email',
                       validators=[DataRequired()])
    submit = SubmitField('Subscribe')

class LogsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/logs.html')
    

class ScoreForm(FlaskForm):
    add_or_subtract = SelectField('ქულის დამატება გინდა თუ გამოკლება?', choices=[(1, 'დამატება (+)'), (0, 'გამოკლება (-)')])
    score = SelectField('აირჩიე ქულა', choices=[(5, '5'), (10, '10'), (15, '15'), (20, '20'), (50, '50'), (100, '100')],
                        validators=[DataRequired()])
    description = TextAreaField('რატომ უმატებთ/აკლებთ ქულას?',
                                validators=[DataRequired(), Length(min=20, max=100)])
    
    submit = SubmitField('Submit')