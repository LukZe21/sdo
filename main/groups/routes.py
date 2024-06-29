from flask import Blueprint
from flask_login import current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request
from main import db
from main.models import User, Group, GroupLogs, NotificationLogs
from main.groups.forms import UpdateGroupForm
from main.forms import ScoreForm
from main.groups.utils import save_picture
from main.exp_se import search_engine

groups = Blueprint('groups', __name__)

def add_log(id="", log="", user_id="", user_log=""):
    if user_id != "" and user_log != "":
        new_notification = NotificationLogs(user_id=user_id, log=user_log)
        db.session.add(new_notification)
    elif id != "" and log != "":
        log = GroupLogs(group_id=id, log=log)
        db.session.add(log)
    db.session.commit()

@groups.route('/search_result/<string:query>', methods=['GET', 'POST'])
def handle_search(query):
    if query:
        users = User.query.all()
        groups = Group.query.all()
        users, groups = search_engine(query, users, groups)
        print(users, groups)
        query = request.form.get('query')
        if request.form.get('entity') == 'გუნდები':
            return render_template('search.html', results=groups)
        else:
            return render_template('search.html', results=users)

@groups.route('/handle_notification', methods=['POST'])
def handle_notification():
    notification_id = request.form.get('notification_id')
    group_id = request.form.get('group_id')
    action = request.form.get('action')

    notification = NotificationLogs.query.filter_by(id=notification_id).first()

    if action == "accept" and current_user.in_group:
        flash("You are already in a team", "danger")
        return redirect(url_for('groups.groups_section'))

    elif action == "accept" and not current_user.in_group:
        user_id = current_user.id
        user = User.query.get(user_id)
        group = Group.query.filter_by(id=group_id).first()
        group.members.append(user)
        user.in_group = True
        flash('Successfully joined the group!', 'success')
        db.session.delete(notification)
        db.session.commit()
        log_msg = f"{current_user.firstname} {current_user.lastname} (@{current_user.nickname}) შემოვიდა გუნდში"
        add_log(group_id, log_msg)

        return redirect(url_for('groups.group_page', id=group_id))
    
    elif action == "decline":
        db.session.delete(notification)
        db.session.commit()
    
    return redirect(url_for('groups.groups_section'))

@groups.route('/groups', methods=['POST', 'GET'])
def groups_section():
    groups = Group.query.all()
    if request.method == "POST":
        if request.form.get("category") == 'ყველა':
            groups = Group.query.all()
        elif request.form.get("category") == 'ტექნოლოგიები & ინოვაციები':
            groups = Group.query.filter_by(category='ტექნოლოგიები & ინოვაციები').all()
        elif request.form.get("category") == 'არაფორმალური განათლება':
            groups = Group.query.filter_by(category='არაფორმალური განათლება').all()
        elif request.form.get("category") == 'მარკეტინგი':
            groups = Group.query.filter_by(category='მარკეტინგი').all()
        elif request.form.get("category") == 'სპორტი':
            groups = Group.query.filter_by(category='სპორტი').all()
    query = request.form.get('query')
    if query:
        return redirect(url_for('groups.handle_search', query=query))
    try:
        page = request.args.get('page', 1, type=int)
        notification_log = NotificationLogs.query.filter_by(user_id=current_user.id).order_by(NotificationLogs.id.desc())
        group_logs = GroupLogs.query.filter_by(group_id=current_user.group_id).order_by(GroupLogs.id.desc()).paginate(page=page, per_page=5)

        return render_template('groups_section.html', groups=groups, group_logs=group_logs, notification_log=notification_log)
    except:
        None
    return render_template('groups_section.html', groups=groups)

@groups.route('/groups/<int:id>', methods=['POST', 'GET'])
def group_page(id):
    group = Group.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    leader = User.query.filter_by(unique_id=group.leader_id).first()
    try:
        group_logs = GroupLogs.query.filter_by(group_id=current_user.group_id).order_by(GroupLogs.id.desc()).paginate(page=page, per_page=5)
        notification_log = NotificationLogs.query.filter_by(user_id=current_user.id).order_by(NotificationLogs.id.desc())

        if current_user.unique_id == group.leader_id:
            group.assign_rank()

        return render_template('group_page.html', group=group, leader=leader, group_logs=group_logs, notification_log=notification_log)
    except:
        group_logs = GroupLogs.query.filter_by(group_id=id).order_by(GroupLogs.id.desc()).paginate(page=page, per_page=5)

    # if request.method == "POST":
    #     try:
    #         user_id = current_user.id
    #         user = User.query.get(user_id)
    #         group.members.append(user)
    #         user.in_group = True
    #         db.session.commit()
    #         flash('Successfully joined the group!', 'success')
    #     except:
    #         flash('You must be logged in to send a request to join the group', 'warning')
    #         return redirect(url_for('users.login'))
    return render_template('group_page.html', group=group, leader=leader, group_logs=group_logs)

@groups.route('/leave_group/<int:id>', methods=['POST', 'GET'])
def leave_group(id):
    group = Group.query.filter_by(id=id).first()
    user = User.query.get(current_user.id)
    if user in group.members:
        user.in_group = False
        user.group_id = None
        user.group = None
        db.session.commit()
        flash('Successfully left the group', 'warning')
    
    log_msg = f"({user.id}) {user.firstname} {user.lastname} (@{current_user.nickname}) გავიდა გუნდიდან"

    add_log(id, log_msg)
    return redirect(url_for('groups.group_page', id=id))

@groups.route('/groups/<int:id>/control_panel', methods=['POST', 'GET'])
def control_panel(id):
    page = request.args.get('page', 1, type=int)
    group = Group.query.filter_by(id=id).first()
    form = UpdateGroupForm()
    try:
        group_logs = GroupLogs.query.filter_by(group_id=current_user.group_id).order_by(GroupLogs.id.desc()).paginate(page=page, per_page=5)
        group = Group.query.filter_by(id=id).first()
        notification_Log = NotificationLogs.query.filter_by(user_id=current_user.id).order_by(NotificationLogs.id.desc())
    except:
        None
    try:
        if current_user.unique_id == group.leader_id or (current_user.rank == 'თანახელმძღვანელი' and current_user in group.members):
            None
        else:
            flash("You are not this group's leader", 'danger')
            return redirect(url_for('groups.groups_section'))
        
    except AttributeError:
        flash("You are not this group's leader", 'danger')
        return redirect(url_for('groups.groups_section'))
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            group.image_file = picture_file
        group.description = form.description.data
        group.group_form = form.group_form.data
        flash("Successfully updated", 'success')
        db.session.commit()
        return redirect(url_for("groups.group_page", id=id))
    elif request.method == "GET":
        form.description.data = group.description
        form.group_form.data = group.group_form
    image_file = url_for('static', filename='imgs/team_pics/' + group.image_file)

    return render_template('control_panel.html', group=group, group_logs=group_logs, notification_log=notification_Log,
                           form=form, image_file=image_file)

@groups.route('/groups/<int:id>/member/<int:member_id>', methods=['POST', 'GET'])
def member_control_panel(id, member_id):
    form = ScoreForm()
    user = User.query.get(member_id)
    group = Group.query.filter_by(id=id).first()
    try:
        page = request.args.get('page', 1, type=int)
        group_logs = GroupLogs.query.filter_by(group_id=current_user.group_id).order_by(GroupLogs.id.desc()).paginate(page=page, per_page=5)
        notification_log = NotificationLogs.query.filter_by(user_id=current_user.id).order_by(NotificationLogs.id.desc())
    except:
        None
    try:
        if current_user.unique_id == group.leader_id or (current_user.rank == 'თანახელმძღვანელი' and current_user in group.members):
            None
        else:
            flash("You are not this group's leader", 'danger')
            return redirect(url_for('groups.groups_section'))
        
    except AttributeError:
        flash("You are not this group's leader", 'danger')
        return redirect(url_for('groups.groups_section'))

    if form.validate_on_submit():
        if form.add_or_subtract.data == '1':
            user.score += int(form.score.data)
            db.session.commit()
            flash(f'თქვენ დაუმატეთ {form.score.data} ქულა {user.firstname} {user.lastname} (@{user.nickname})-ს', 'success')

            log_msg = f"{user.firstname} {user.lastname}-ს დაემატა {form.score.data} ქულა.\n მიზეზი: {form.description.data}"
            
            new_log= f"თქვენ დაგემატათ {form.score.data} ქულა!\n მიზეზი: {form.description.data}"
            user_id = user.id
            add_log(id, log_msg, user_id, new_log)

            return redirect(url_for("groups.control_panel", id=id))

        elif form.add_or_subtract.data == '0':
            if user.score - int(form.score.data) >= 0:
                user.score -= int(form.score.data)
                print(user.score)
                db.session.commit()
                flash(f'თქვენ ჩამოაჭერით {form.score.data} ქულა {user.firstname} {user.lastname} (@{user.nickname})-ს', 'success')

                log_msg = f"{user.firstname} {user.lastname} (@{user.nickname})-ს ჩამოეჭრა {form.score.data} ქულა.\n\n\n მიზეზი: {form.description.data}"

                add_log(id, log_msg)

                return redirect(url_for("groups.control_panel", id=id))
            else:
                flash(f'წევრის ქულას 0-ზე დაბლა ვერ ჩამოიყვანთ.', 'danger')
    return render_template('personal_score_panel.html', user=user, form=form, group_logs=group_logs, notification_log=notification_log, group=group)

@groups.route('/groups/<int:id>/add_member', methods=['POST'])
def add_member(id):
    group = Group.query.filter_by(id=id).first()
    user_id = request.form.get('ID')
    print(user_id)
    user = User.query.filter_by(unique_id=user_id).first()
    if not user:
        flash("Please enter valid user ID", 'danger')
    elif len(group.members) >= 10:
        flash('Your team is full', 'danger')
    elif user.in_group:
        flash(f"{user.firstname} {user.lastname} (@{user.nickname}) is already in a team", 'danger')
    elif not user.in_group:
        flash(f"Invitation has been successfully sent to {user.firstname} {user.lastname} (@{user.nickname}).", "success")
        new_notification = NotificationLogs(user_id=user.id, group_id=group.id, log=f"{group.name}-მა მოგიწვიათ თავიანთ გუნდში")
        db.session.add(new_notification)
        db.session.commit()

    return redirect(url_for('groups.control_panel', id=id))

@groups.route('/remove_member/<int:member_id>', methods=['POST'])
def remove_member(member_id):
    user = User.query.get(member_id)
    user.in_group = False
    group_id = user.group_id
    log_msg = f"{user.firstname} {user.lastname} (@{user.nickname}) გააგდეს ჯგუფიდან."

    user_msg = f"თქვენ გაგაგდეს გუნდიდან"
    add_log(group_id , log_msg, user.id, user_msg)
    
    user.group_id = None
    user.group = None
    flash(f'Successfully removed {user.firstname} {user.lastname} (@{user.nickname}) from the group', 'warning')    
    return redirect(url_for('groups.control_panel', id=group_id))


@groups.route('/groups/<int:member_id>/make_member_leader', methods=['POST'])
def make_leader(member_id):
    user = User.query.get(member_id)
    group = Group.query.get(user.group_id)
    previous_leader = User.query.filter_by(unique_id=group.leader_id).first()
    previous_leader.rank = 'თანახელმძღვანელი'
    user.rank = 'ხელმძღვანელი'
    group.leader_id = user.unique_id
    add_log(user_id=user.id, user_log=f"თქვენ გახდით გუნდის ახალი ხელმძღვანელი!")
    db.session.commit()
    
    return redirect(url_for('groups.group_page', id=group.id))

@groups.route('/groups/<int:member_id>/make_member_coleader', methods=['POST'])
def make_coleader(member_id):
    user = User.query.get(member_id)
    group = Group.query.get(user.group_id)
    user.rank = 'თანახელმძღვანელი'
    add_log(user_id=user.id, user_log=f"თქვენ გახდით გუნდის თანახელმძღვანელი")
    db.session.commit()

    return redirect(url_for('groups.control_panel', id=group.id))


@groups.route('/groups/<int:id>/change_name', methods=['POST'])
def change_name(id):
    group = Group.query.filter_by(id=id).first()
    new_name = request.form.get('group_name')
    old_name = group.name
    group.name = new_name
    
    log_msg = f"ჯგუფის სახელი შეიცვალა: {old_name} (ძველი) -> {group.name} (ახალი)"

    add_log(id, log_msg)
    
    return redirect(url_for('groups.control_panel', id=id))


@groups.route('/groups/<int:id>/delete_team', methods=['POST'])
def delete_team(id):
    group = Group.query.get_or_404(id)
    for member in group.members:
        member.in_group = False
        member.group_id = None
        user_msg = f"თქვენი გუნდი გაუქმდა"
        add_log(user_id=member.id, user_log=user_msg)
        member.group = None
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('groups.groups_section'))