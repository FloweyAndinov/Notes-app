from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
auth = Blueprint('auth' , __name__)
from flask_login import login_user, login_required, logout_user, current_user





#login logic
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username')
        print(user_name)
        password = request.form.get('password')
        print(password)
        user = User.query.filter_by(username=user_name).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid credentials', category='error')
    return render_template("login.html", user=current_user)




#logout logic
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect (url_for('auth.login'))



#sign up logic
@login_required
@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        username = request.form.get('username')
        print(generate_password_hash(password1, method='sha256'))

        if User.query.filter_by(email=email).first():
            flash('Account with this email already exists', category='error')
        elif len(username) < 4:
            flash('Invalid username', category='error')
        elif len(password1) < 4:
            flash('Invalid password', category='error')
        elif len(email) < 4:
            flash('Invalid Email', category='error')
        elif password1!= password2:
            flash('Passwords don\'t match', category='error')
            pass
        else:
            #add user to database
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), username=username)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html" , user=current_user)