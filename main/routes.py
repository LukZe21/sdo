from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from main.forms import DiscountElementForm, eventElementForm, LoginForm, emailForm, RegisterForm, DiscountElementView, EventElementView, LogsView, UserView, GroupView
from flask_admin.contrib.sqla import ModelView
from main.models import discountElement, eventElement, User, email, Group
from werkzeug.utils import secure_filename
import os
from main import db, app, serializer, mail, bcrypt, admin
from flask_mail import Message
import random
from datetime import datetime
import json
from main.auto_correction import process_text
from main.search_system import search_query
from main.email_sender import send_emails


# Adding Views to admin page
admin.add_view(DiscountElementView(discountElement, db.session))
admin.add_view(EventElementView(eventElement, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(GroupView(Group, db.session))
admin.add_view(LogsView(name='Logs', endpoint='logs'))


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


def send_activation_email(user_email):
    token = serializer.dumps(user_email, salt='email-confirmation-salt')
    activation_link = url_for('activation_account', token=token, _external=True)

    msg = Message('Account Activation', sender='ldzotsenidze4@gmail.com', recipients=[user_email])
    msg.body = f"To activate your account and get updated when new events/discounts get added, click the following link {activation_link}\nIf you are'nt the one who tried to activate account on our website feel free to ignore this message."

    mail.send(msg)

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def main():
    discount_elements = discountElement.query.all()
    event_elements = eventElement.query.all()
    emails = [email.email for email in email.query.all()]
    email_form = emailForm()

    # shuffling elements
    random.shuffle(discount_elements)
    random.shuffle(event_elements)


    # email verification 
    if email_form.validate_on_submit():
        if email_form.email.data not in emails:
            send_activation_email(email_form.email.data)
            flash('A confirmation email has been sent to your email address.', 'success')
        else:
            flash('Email has already subscribed', 'warning')

    # search system
    user_query = request.args.get('query')
    if user_query:
        processed_text = process_text(user_query)
        search_results = search_query(processed_text, discount_elements, event_elements)
        print(search_results)
        return render_template('search_results.html', text=processed_text)


    return render_template("index1.html", discount_elements=discount_elements, event_elements=event_elements, email_form=email_form)


# account activation
@app.route('/activation/<token>')
def activation_account(token):
    email_address = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    user_email = email(email=email_address)
    db.session.add(user_email)
    db.session.commit()
    flash("Your account has been activated!", 'success')
    return redirect(url_for('main'))

# All discount functionalities

@app.route("/discount/<string:id>", methods=["POST", "GET"])
def discount_element(id):
    discount_info = discountElement.query.filter_by(id=id).first()
    expiration_duration = discount_info.expiration_duration - datetime.now() 
    print(expiration_duration)
    return render_template('discount_page.html', discount_info=discount_info, expiration_duration=expiration_duration.days)

@app.route("/discount/<string:id>/update", methods=["POST", "GET"])
def update_discount_element(id):
    discount_element = discountElement.query.get_or_404(id)
    discount_form = DiscountElementForm()
    if discount_form.validate_on_submit():
        discount_element.name = discount_form.name.data
        discount_element.condition = discount_form.condition.data
        discount_element.description = discount_form.description.data 
        discount_element.categories = discount_form.categories.data
        discount_element.expiration_duration = discount_form.expiration_duration.data
        db.session.commit()
        flash(f"Successfully updated {discount_element.name} discount element!", 'success')
        return redirect(url_for('discount_element', id=discount_element.id))
    
    elif request.method == "GET":
        discount_form.name.data = discount_element.name
        discount_form.condition.data = discount_element.condition
        discount_form.description.data = discount_element.description
        discount_form.categories.data = discount_element.categories
        discount_form.expiration_duration.data = discount_element.expiration_duration
        discount_id = discount_element.id
    
    return render_template('discount_update.html', discount_form=discount_form, discount_id=discount_id)

@app.route("/discount/<int:id>/delete", methods=['POST'])
def delete_discount(id):
    discount_element = discountElement.query.get_or_404(id)
    db.session.delete(discount_element)
    db.session.commit()
    flash("Successfuly deleted discount element!", 'success')
    return redirect(url_for('main'))

# All event functionalities

@app.route("/event/<int:id>", methods=["POST", "GET"])
def event_element(id):
    event_info = eventElement.query.filter_by(id=id).first()
    event_duration = int((event_info.end_date - event_info.start_date).total_seconds() / 3600)
    return render_template('event_page.html', event_info=event_info, event_duration=event_duration)

@app.route("/event/<int:id>/update", methods=["POST", "GET"])
@login_required
def update_event_element(id):
    event_element = eventElement.query.get_or_404(id)
    event_form = eventElementForm()
    if event_form.validate_on_submit():
        event_element.name = event_form.name.data
        event_element.description = event_form.description.data
        event_element.categories = event_form.categories.data
        event_element.start_date = event_form.start_date.data
        event_element.end_date = event_form.end_date.data
        event_element.event_hoster = event_form.event_hoster.data
        event_element.location = event_form.location.data
        db.session.commit()
        flash(f"Successfully updated {event_element.name} discount element!", 'success')
        return redirect(url_for('event_element', id=event_element.id))
    
    elif request.method == "GET":
        event_form.name.data= event_element.name
        event_form.description.data = event_element.description
        event_form.categories.data = event_element.categories
        event_form.start_date.data = event_element.start_date
        event_form.end_date.data = event_element.end_date
        event_form.event_hoster.data = event_element.event_hoster
        event_form.location.data = event_element.location
        event_id = event_element.id
    return render_template('event_update.html', event_form=event_form, event_id=event_id)


@app.route("/event/<int:id>/delete", methods=['POST'])
def delete_event(id):
    event_element = eventElement.query.get_or_404(id)
    db.session.delete(event_element)
    db.session.commit()
    flash("Successfuly deleted event element!", 'success')
    return redirect(url_for('main'))


@app.route('/discounts', methods=['POST', 'GET'])
def discounts_page():
    discount_elements = discountElement.query.all()
    filtered_elements = []
    if request.method == 'POST':
        category = request.form.get('category')
        if category != 'ყველა':
            for discount_element in discount_elements:
                if category in discount_element.categories:
                    filtered_elements.append(discount_element)
            return render_template('discounts_section.html', discount_elements=filtered_elements)
    return render_template('discounts_section.html', discount_elements=discount_elements)

@app.route('/events', methods=['POST', 'GET'])
def events_page():
    event_elements = eventElement.query.all()
    filtered_elements = []
    if request.method == 'POST':
        category = request.form.get('category')
        if category != 'ყველა':
            for event_element in event_elements:
                if category in event_element.categories:
                    filtered_elements.append(event_element)
            return render_template('events_section.html', event_elements=filtered_elements)
    return render_template('events_section.html', event_elements=event_elements)

@app.route('/student_events', methods=['POST', 'GET'])
def students_event_page():
    student_events = eventElement.query.filter_by(type='1').all()
    print(student_events)
    return render_template('students.html', events=student_events)

@app.route('/sponsor_events', methods=['POST', 'GET'])
def sponsors_event_page():
    sponsor_events = eventElement.query.filter_by(type='0').all()
    return render_template('sponsors.html', events=sponsor_events)


@app.route('/groups', methods=['POST', 'GET'])
def groups_section():
    groups = Group.query.all()
    return render_template('groups_section.html', groups=groups)

@app.route('/group_page/<int:id>', methods=['POST', 'GET'])
def group_page(id):
    group = Group.query.filter_by(id=id).first()
    print(group.members)
    leader = User.query.get(group.leader_id)
    if request.method == "POST":
        try:
            user_id = current_user.id
            user = User.query.get(user_id)
            group.members.append(user)
            user.in_group = True
            db.session.commit()
            flash('Successfully joined the group!', 'success')
        except:
            flash('You must be logged in to send a request to join the group', 'success')
            return redirect(url_for('login'))
    return render_template('group_page.html', group=group, leader=leader)

@app.route('/leave_group/<int:id>', methods=['POST', 'GET'])
def leave_group(id):
    group = Group.query.filter_by(id=id).first()
    user = User.query.get(current_user.id)
    if user in group.members:
        user.in_group = False
        user.group_id = None
        user.group = None
        db.session.commit()
        flash('Successfully Left the group', 'warning')
    return redirect(url_for('group_page', id=id))

@app.route('/registration', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    
        add_user_info({
            "email": form.email.data,
            "password": form.password.data
        })

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register_page.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('groups_section'))
        else:
            flash('Login Unsuccessful.', 'danger')

    return render_template('login_page.html', form=form)

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')

@app.route("/logout")
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('main'))