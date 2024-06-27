from flask import Blueprint, render_template, request
from main.models import discountElement, eventElement
from datetime import datetime

elements = Blueprint('elements', __name__)


@elements.route('/discounts', methods=['POST', 'GET'])
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

@elements.route("/discount/<string:id>", methods=["POST", "GET"])
def discount_element(id):
    discount_info = discountElement.query.filter_by(id=id).first()
    expiration_duration = discount_info.expiration_duration - datetime.now() 
    print(expiration_duration)
    return render_template('discount_page.html', discount_info=discount_info, expiration_duration=expiration_duration.days)


@elements.route('/events', methods=['POST', 'GET'])
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

@elements.route("/event/<int:id>", methods=["POST", "GET"])
def event_element(id):
    event_info = eventElement.query.filter_by(id=id).first()
    event_duration = int((event_info.end_date - event_info.start_date).total_seconds() / 3600)
    return render_template('event_page.html', event_info=event_info, event_duration=event_duration)


@elements.route('/student_events', methods=['POST', 'GET'])
def students_event_page():
    student_events = eventElement.query.filter_by(type='1').all()
    print(student_events)
    return render_template('students.html', events=student_events)

@elements.route('/sponsor_events', methods=['POST', 'GET'])
def sponsors_event_page():
    sponsor_events = eventElement.query.filter_by(type='0').all()
    return render_template('sponsors.html', events=sponsor_events)