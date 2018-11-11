from flask import Blueprint, redirect, render_template, request
from monolith.database import db, User, Run, _delete_user
from monolith.auth import admin_required
from monolith.forms import UserForm, DeleteForm
from flask_login import current_user, logout_user


users = Blueprint('users', __name__)


@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(form.password.data) #pw should be hashed with some salt
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

    return render_template('create_user.html', form=form)

@users.route("/delete_user", methods=['GET', 'POST'])
def delete_user():
    form = DeleteForm()
    try:
        email = current_user.email
    except AttributeError:
        return redirect('/login')

    if form.validate_on_submit():
        #verify user password
        password = form.data['password']
        q = db.session.query(User).filter(User.id == current_user.id)
        user = q.first()

        if user is not None and user.authenticate(password):
            logout_user()
            #delete the user and all his data
            _delete_user(user)
            return redirect('/users')

    return render_template('delete_user.html', form=form, user_email=email)
