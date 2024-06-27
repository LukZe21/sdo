from main import db, app, serializer, mail
from flask_mail import Message
from flask import redirect, url_for, flash
from main.models import email
import json
import secrets
import os
from PIL import Image

def load_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def add_user_info(user_data):
    file_path = 'main/static/user_data.json'
    current_data = load_json(file_path)

    current_data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(current_data, file, indent=2)

def send_activation_email(email, token):
    msg = Message('Account Activation', sender='ldzotsenidze4@gmail.com', recipients=[email])
    msg.body = f'Please click the following link to activate your account: {url_for("users.activate", token=token, _external=True)}'
    mail.send(msg)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/imgs/profile_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# def send_activation_email(user_email):
#     token = serializer.dumps(user_email, salt='email-confirmation-salt')
#     activation_link = url_for('activation_account', token=token, _external=True)

#     msg = Message('Account Activation', sender='ldzotsenidze4@gmail.com', recipients=[user_email])
#     msg.body = f"To activate your account and get updated when new events/discounts get added, click the following link {activation_link}\nIf you are'nt the one who tried to activate account on our website feel free to ignore this message."

#     mail.send(msg)

# # account activation
# @app.route('/activation/<token>')
# def activation_account(token):
#     email_address = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
#     user_email = email(email=email_address)
#     db.session.add(user_email)
#     db.session.commit()
#     flash("Your account has been activated!", 'success')
#     return redirect(url_for('main'))