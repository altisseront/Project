from flask_app.models.user import User
from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route ('/')
def index():
    return render_template('login.html')
@app.route('/register_user', methods = ['POST'])
def create_user():
    if not User.validate_user(request.form, User.get_all()):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = { "email" : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email/password', "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["pword"]):
        flash('Invalid Email/password', "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard ():
    if 'user_id' not in session:
        flash('You must log in first!')
        return redirect ('/')
    data = { "user_id" : session['user_id']}
    return render_template('dashboard.html', user=User.get_user_by_id(data), all_users_but = User.get_all_but(session['user_id']), follows = User.follows(data), feed = User.get_feed(data), hasliked = User.has_liked(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/follow/<int:followed_id>')
def follow(followed_id):
    data = {
        "user_id" : session['user_id'],
        "followed_id" : followed_id
    }
    User.follow_user(data)
    return redirect('/dashboard')

@app.route('/unfollow/<int:followed_id>')
def unfollow(followed_id):
    data = {
        "user_id" : session['user_id'],
        "followed_id" : followed_id
    }
    User.unfollow_user(data)
    return redirect('/dashboard')
