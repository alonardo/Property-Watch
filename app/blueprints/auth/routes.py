from flask import render_template, request, redirect, url_for, flash
from app.models import User
from flask_login import login_user, login_required, logout_user, current_user
from app.blueprints.auth.forms import EditProfileForm, LoginForm, RegisterForm
from . import bp as auth

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print('Code is here!')
    if request.method == 'POST':
        print('POST successful!')
        if form.validate_on_submit():
            print('I"M TRYING TO RUN!!!')
            try:
                new_user_data={
                    "first_name": form.first_name.data.title(),
                    "last_name": form.last_name.data.title(),
                    "email": form.email.data.lower(),
                    "password" : form.password.data,
                    "icon":form.icon.data
                }
                new_user_object = User()
                new_user_object.from_dict(new_user_data)
                new_user_object.save()
            except:
                print('I"M IN THE EXCEPT!')
                # Flash user Error
                flash("An Unexpected Error occurred", "danger")
                return render_template('register.html.j2', form=form)
            # Flash user here telling you have been register
            flash("Successfully registered, welcome to Pokemon Search! Please login to continue.", "success")
            return redirect(url_for('auth.login'))

    return render_template('register.html.j2', form=form)

@auth.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        edited_user_data={
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
                "icon":int(form.icon.data) if int(form.icon.data) != 9000 else current_user.icon
            }
        user = User.filter_by(email=edited_user_data['email']).first()
        if user and user.email != current_user.email:
            flash('Email already exists!', 'danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(edited_user_data)
            current_user.save()
            flash('Profile updated!', 'success')
        except:
            flash('Error updating profile!', 'danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))
    return render_template('register.html.j2', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print('login POST success')
        if form.validate_on_submit():
            email = form.email.data.lower()
            print(email)
            password = form.password.data
            print(password)

            u = User.query.filter_by(email=email).first()
            print('form validated!!')
            if u:
                print('u printed')
            if u.check_hashed_password(password):
                print('u.check printed')
                flash('Successfully logged in','success')
                login_user(u)
                return redirect(url_for('main.index'))
            flash("Incorrect Email/password Combo", "warning")
            return render_template('login.html.j2', form=form)

    return render_template('login.html.j2', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'info')
    return redirect(url_for('main.index'))
