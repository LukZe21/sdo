from flask import Blueprint, render_template, request, flash, redirect, url_for
from main.models import discountElement, eventElement, User, email, Group, GroupLogs, FormData
from main.elements.forms import DiscountElementView, EventElementView
from main.groups.forms import GroupView
from main.users.forms import UserView
from main.forms import emailForm, MemberForm, LeaderForm, LogsView
# from main.other.utils import send_activation_email
from flask_mail import Message
from main.auto_correction import process_text
from main.search_system import search_query
from main import db, admin, bcrypt, mail, csrf
import random
import secrets

other = Blueprint('other', __name__)

admin.add_view(DiscountElementView(discountElement, db.session))
admin.add_view(EventElementView(eventElement, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(GroupView(Group, db.session))
admin.add_view(LogsView(name='Logs', endpoint='logs'))


@other.route("/", methods=['POST', 'GET'])
@other.route("/home", methods=['POST', 'GET'])
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
            # send_activation_email(email_form.email.data)
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

@csrf.exempt
@other.route('/fill_path', methods=['POST', 'GET'])
def fill_path():
    if request.method == 'POST':
        if request.form.get('entity') == 'MEMBER':
            return redirect(url_for('other.fill_form_member'))
        
    return render_template('fill_path.html')

@csrf.exempt
@other.route('/fill_form_member', methods=['POST', 'GET'])
def fill_form_member():
    form = MemberForm()
    teams = Group.query.all()
    form.team.choices = [(team.id, f"{team.name}, სამსახური - {team.category}") for team in teams if len(team.members) < 5]
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if not existing_user:
            form_data = FormData(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                why_join=form.why_join.data,
                category=form.category.data,
                facebook_link=form.facebook_link.data
            )
            db.session.add(form_data)
            db.session.commit()
            flash('წარმატებით გაიგზავნა ანკეტა, კვალიფიკაციის შემთხვევაში დაგეკონტაქტებით ელფოსტის მეშვეობით.', 'success')
        elif existing_user:
            flash('ელფოსტა დაკავებულია, გთხოვთ სხვა ელფოსტა ჩაწეროთ.', 'danger')
            return redirect(url_for('other.fill_form_member'))

        return redirect(url_for('other.main'))
    return render_template('fill_form.html', form=form, teams=teams)

@other.route('/applied_forms', methods=['POST', 'GET'])
def applied_forms():
    form_data = FormData.query.all()

    return render_template('applied_forms.html', forms=form_data)

@csrf.exempt
@other.route('/user_form/<int:id>', methods=['POST', 'GET'])
def form(id):
    user_form = FormData.query.get(id)
    if request.method == 'POST':
        try:
            if request.form.get('entity') == 'ACCEPT':
                password = secrets.token_hex(16)
                unique_id = secrets.token_hex(8)
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user = User(unique_id=unique_id, firstname=user_form.firstname, lastname=user_form.lastname,
                            facebook_link=user_form.facebook_link, email=user_form.email, password=hashed_password)
                db.session.add(user)
                db.session.delete(user_form)
                db.session.commit()
                msg = Message('Account Activation', sender='ldzotsenidze4@gmail.com', recipients=[user_form.email])
                msg.body = f'FULL INFO: email: {user_form.email}\npassword: {password}'
                mail.send(msg)

                flash('წარმატებით გაეგზავნა ინფორმაცია მომხმარებელს', 'success')
                return redirect(url_for('other.applied_forms'))

            elif request.form.get('entity') == 'DECLINE':
                db.session.delete(user_form)
                db.session.commit()

                flash('მომხმარებლის განაცხადი უარყოფილია', 'info')
                return redirect(url_for('other.applied_forms'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erorr {str(e)}", 'danger')

    return render_template('user_form.html', form=user_form)