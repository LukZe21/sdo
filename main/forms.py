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


class MemberForm(FlaskForm):
    firstname = StringField('სახელი', validators=[DataRequired()])
    lastname = StringField('გვარი', validators=[DataRequired()])
    email = EmailField('ელფოსტა', validators=[DataRequired()])
    why_join = TextAreaField('რატომ გინდათ ამ პროექტში მონაწილეობა')
    # category = SelectField('სამსახური', choices=[
                                    #     ('სპორტის კულტურის და ახალგზარდობის სამსახური', 'სპორტის კულტურის და ახალგზარდობის სამსახური'),
                                    #     ('არაფორმალური განათლება', 'არაფორმალური განათლება'),
                                    #     ('ტექნოლოგიები და ინოვაციები', 'ტექნოლოგიები და ინოვაციები'),
                                    #     ('PR და მარკეტინგი', 'PR და მარკეტინგი')
                                    # ])
    
    team = SelectField('აირჩიე სამუშაო გუნდი', choices=[], coerce=int)  # Dropdown for teams
    facebook_link = StringField('შენი Facebook პროფილის ლინკი', validators=[DataRequired()])
    submit = SubmitField("გააგზავნე ანკეტა")


class LeaderForm(FlaskForm):
    firstname = StringField('სახელი', validators=[DataRequired()])
    lastname = StringField('გვარი', validators=[DataRequired()])
    email = EmailField('ელფოსტა', validators=[DataRequired()])
    why_join = TextAreaField('რატომ გინდათ ამ პროექტში მონაწილეობა')
    category = SelectField('სამსახური', choices=[('სპორტის კულტურის და ახალგზარდობის სამსახური', 'არაფორმალური განათლება', 'ტექნოლოგიები და ინოვაციები', 'PR და მარკეტინგი')])
    team_name = StringField('გუნდის სახელი', validators=[DataRequired()])
    submit = SubmitField("გააგზავნე ანკეტა")