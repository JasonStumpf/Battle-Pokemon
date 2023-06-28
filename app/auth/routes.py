from flask import Blueprint, render_template, request, redirect, url_for
from .forms import SignupForm, LoginForm
from ..models import User
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User(email,password)
            user.save_user()

            return redirect(url_for('auth.login'))
        
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    print("Incorrect Password")
            else:
                print("That user does not exist")


    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))