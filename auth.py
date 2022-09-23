
from flask_login import login_user,login_required,logout_user
from flask import flash, redirect, render_template,Blueprint,Flask, request, url_for
from werkzeug.security import check_password_hash,generate_password_hash
from . import db
from .dbModels import User
auth = Blueprint('auth',__name__)

@auth.route('/signUp')
def signUp():
    return render_template('signUp.html')

@auth.route('/signUp',methods = ['POST'])
def signUpPost():
    name = request.form.get('name')
    password = request.form.get('password')
    email = request.form.get('email')
    user = User.query.filter_by(email = email).first()
    print(name,password,email)
    if user:
        flash('Emai address already exists')
        return redirect(url_for('auth.signUp'))
    new_user = User(email= email,name = name,password = generate_password_hash(password= password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def login_post():
    password = request.form.get('password')
    email = request.form.get('email')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email= email).first()
    if not user or not check_password_hash(user.password,password):
        flash('wrong login details')
        return redirect(url_for('auth.login'))

    login_user(user,remember = remember)
    return redirect(url_for('main.profile'))
    
@auth.route('/logOut')
@login_required
def logOut():
    logout_user()
    return redirect(url_for('main.home'))