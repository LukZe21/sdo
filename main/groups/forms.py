from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from flask_admin.contrib.sqla import ModelView

class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    category = SelectField('Category', choices=[
        ('მარკეტინგი', 'მარკეტინგი'), 
        ('არაფორმალური განათლება', 'არაფორმალური განათლება'), 
        ('სპორტი', 'სპორტი'), 
        ('ტექნოლოგიები და ინოვაციები', 'ტექნოლოგიები და ინოვაციები')
    ])
    leader_id = StringField('ლიდერის ID', validators=[DataRequired()])

    group_form = StringField("Submittion Form Link", validators=[DataRequired()])

    score = IntegerField('Score', validators=[DataRequired()], default=100)

class GroupView(ModelView):
    form = GroupForm
    form_extra_fields = {
        'members': TextAreaField('Members', description="შეიყვანე ჯგუფის წევრები მძიმეების(,) გამოყოფით.")
    }
    form_columns = ('name', 'description', 'category', 'members', 'score', 'group_form')

    def on_model_change(self, form, model, is_created):
        if 'members' in form.data:
            model.members_list = [member.strip() for member in form.members.data.split(',')]
        return super(GroupView, self).on_model_change(form, model, is_created)
    

class UpdateGroupForm(FlaskForm):
    description = TextAreaField('გუნდის შესახებ')

    leader_id = StringField('ლიდერის ID', validators=[DataRequired()])

    group_form = StringField("Submittion Form Link", validators=[DataRequired()])

    picture = FileField('Update Banner', validators=[FileAllowed(['jpg', 'png'])])


    submit = SubmitField("Update")
