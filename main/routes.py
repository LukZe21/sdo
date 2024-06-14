from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required
from main.forms import DiscountElementForm, eventElementForm, LoginForm, emailForm
from main.models import discountElement, eventElement, User, email
from werkzeug.utils import secure_filename
import os
from main import db, app, serializer, mail
from flask_mail import Message
import random
from datetime import datetime
from main.auto_correction import process_text
from main.search_system import search_query
from main.email_sender import send_emails


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


    if email_form.validate_on_submit():
        if email_form.email.data not in emails:
            send_activation_email(email_form.email.data)
            flash('A confirmation email has been sent to your email address.', 'success')
        #     user_email = email(email=email_form.email.data)
        #     db.session.add(user_email)
        #     db.session.commit()
        #     flash('Succesfully Subscribed', 'success')
        else:
            flash('Email has already subscribed', 'warning')

    user_query = request.args.get('query')
    if user_query:
        processed_text = process_text(user_query)
        search_results = search_query(processed_text, discount_elements, event_elements)
        print(search_results)
        return render_template('search_results.html', text=processed_text)


    return render_template("index1.html", discount_elements=discount_elements, event_elements=event_elements, email_form=email_form)

# @app.route("/search")
# def search():
#     return render_template('search_results.html', text=user_query)

@app.route('/activation/<token>')
def activation_account(token):
    email_address = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    user_email = email(email=email_address)
    db.session.add(user_email)
    db.session.commit()
    flash("Your account has been activated!", 'success')
    return redirect(url_for('main'))

@app.route('/login_to_admin_page', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('add'))
        else:
            flash('login Unsuccessful.', 'danger')

    return render_template('login_page.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('main'))

@app.route("/admin-page", methods=['GET', 'POST'])
@login_required
def add():
    discount_form = DiscountElementForm()
    emails = [email.email for email in email.query.all()]

    # add new discount element
    if discount_form.validate_on_submit():
        img_file = discount_form.img.data
        filename = secure_filename(img_file.filename)
        print(filename)
        
        upload_folder = app.config['UPLOAD_FOLDER']

        img_file.save(os.path.join(upload_folder, filename))
        discount_element = discountElement(name=discount_form.name.data, condition=discount_form.condition.data,
                                           description=discount_form.description.data, categories=discount_form.categories.data,
                                           expiration_duration=discount_form.expiration_duration.data, img=filename)

        flash(f"Successfully added new discount with name {discount_form.name.data}!", "success")
        
        db.session.add(discount_element)
        db.session.commit()

        if discount_form.toggle.data:
            id = discountElement.query.filter_by(name=discount_form.name.data).first().id

            send_emails(category='discount', id=id, name=discount_form.name.data, 
                        condition=discount_form.condition.data,
                        expiration_duration=discount_form.expiration_duration.data, emails=emails)


        return redirect(url_for('add'))


    # add new event element
    event_form = eventElementForm()

    if event_form.validate_on_submit():
        img_file = event_form.img.data
        filename = secure_filename(img_file.filename)
        print(filename)
        
        upload_folder = app.config['UPLOAD_FOLDER']

        img_file.save(os.path.join(upload_folder, filename))
        event_element = eventElement(name=event_form.name.data, description=event_form.description.data,
                                     categories=event_form.categories.data, start_date=event_form.start_date.data,
                                     end_date=event_form.end_date.data, event_hoster=event_form.event_hoster.data,
                                     location=event_form.location.data, type=event_form.dropdown.data, img=filename)

        db.session.add(event_element)
        db.session.commit()

        if event_form.toggle.data:
            id = eventElement.query.filter_by(name=event_form.name.data).first().id
            print(id, emails)
            send_emails(category='event', id=id, name=event_form.name.data, 
                        start_date=event_form.start_date.data,
                        end_date=event_form.end_date.data,
                        event_hoster=event_form.event_hoster.data,
                        emails=emails)

        flash(f"Successfully added new event with name {event_form.name.data}!", "success")
        return redirect(url_for('add'))
    
    # remove discount or event element
    if request.method=="POST":
        form_id = request.form.get('form_id')
        if form_id == 'form1':
            try:
                discount_element_id = request.form.get('discount')
                discount_element = discountElement.query.get(int(discount_element_id))
                db.session.delete(discount_element)
                db.session.commit()
                flash(f"Successfully deleted discount with name {discount_element.name}")
            except:
                return "ID must be a valid number."
        elif form_id == 'form2':
            try:
                event_element_id = request.form.get('event')
                event_element = eventElement.query.get(int(event_element_id))
                db.session.delete(event_element)
                db.session.commit()
                flash(f"Successfully deleted event with name {event_element.name}")
            except:
                return "ID must be a valid number."

    return render_template('add_elements.html', discount_form=discount_form, event_form=event_form)


# Discount functionalities
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

# Event functionalities
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
    student_events = eventElement.query.filter_by(type='საუნივერსიტეტო').all()
    return render_template('students.html', events=student_events)

@app.route('/sponsor_events', methods=['POST', 'GET'])
def sponsors_event_page():
    sponsor_events = eventElement.query.filter_by(type='სპონსორი').all()
    return render_template('sponsors.html', events=sponsor_events)