from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
    }

    id = User.save(data)
    session['user_id'] = id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    user = User.get_one_email(request.form)

    if not user:
        flash("Sorry, this email is invalid. Please try another.", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Sorry, this password is incorrect. Please try again.", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {"id" : session['user_id']}

    user = User.get_one_id(data)

    return render_template("home.html", user = user)

@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {"id" : session['user_id']}

    user = User.get_one_id(data)

    return render_template("profile.html", user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')