from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_admin.contrib.sqla import ModelView
import os
from main import app

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