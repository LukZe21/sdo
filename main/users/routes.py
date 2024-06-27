from flask_login import login_user, logout_user, login_required, current_user
from main.users.forms import LoginForm, RegisterForm, UpdateAccountForm
from main import db, bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash, request
from main.users.utils import add_user_info, send_activation_email, save_picture
from main.models import User, NotificationLogs, GroupLogs
import secrets
from flask_socketio import emit


users = Blueprint('users', __name__)



@users.route('/registration', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('other.main'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        token = secrets.token_hex(16)
        unique_id = secrets.token_hex(8)
        user = User(unique_id=unique_id, firstname=form.firstname.data, lastname=form.lastname.data, nickname=form.nickname.data, email=form.email.data, password=hashed_password, activation_token=token)
        db.session.add(user)
        db.session.commit()

        # send activation email
        send_activation_email(form.email.data, token)
    
        add_user_info({
            "email": form.email.data,
            "password": form.password.data
        })

        flash('Registration successful! Please check your email to activate your account.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register_page.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('other.main'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_active:
                login_user(user)
                print(f"Logged in user: {user.email}")
                flash('You have been logged in!', 'success')
                return redirect(url_for('groups.groups_section'))
            elif not user.is_active:
                flash('You have to activate your account first in order to login', 'danger')
            else:
                flash('Login Unsuccessful.', 'danger')
        except:
            flash('Login Unsuccessful.', 'danger')

    return render_template('login_page.html', form=form)

@users.route('/activate/<token>')
def activate(token):
    print(token)
    user = User.query.filter_by(activation_token=token).first()
    if user:
        user.is_active = True
        user.activation_token = None
        db.session.commit()
        flash("Account activated successfully!", 'success')
        return redirect(url_for('users.login'))
    else:
        flash("Invalid or expired token", 'danger')
        return redirect(url_for('users.register'))

@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    notification_log = NotificationLogs.query.filter_by(user_id=current_user.id)
    page = request.args.get('page', 1, type=int)
    group_logs = GroupLogs.query.filter_by(group_id=current_user.group_id).order_by(GroupLogs.id.desc()).paginate(page=page, per_page=5)
    
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.nickname = form.nickname.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for("users.profile"))
    elif request.method == "GET":
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.nickname.data = current_user.nickname
        form.email.data = current_user.email
    image_file = url_for('static', filename='imgs/profile_pics/' + current_user.image_file)

    return render_template('profile.html', notification_log=notification_log, group_logs=group_logs,
                           image_file=image_file, form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('groups.groups_section'))