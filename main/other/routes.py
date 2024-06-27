from flask import Blueprint, render_template, request, flash
from main.models import discountElement, eventElement, User, email, Group, GroupLogs
from main.elements.forms import DiscountElementView, EventElementView
from main.groups.forms import GroupView
from main.users.forms import UserView
from main.forms import LogsView
from main.forms import emailForm
# from main.other.utils import send_activation_email
from main.auto_correction import process_text
from main.search_system import search_query
from main import db, admin
import random

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