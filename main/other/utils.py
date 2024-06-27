# from main import db, app, serializer, mail
# from flask_mail import Message
# from flask import redirect, url_for, flash
# from main.models import email

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
