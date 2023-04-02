from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.register import Register
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.secret_key = "remember your info"

@app.route("/")
def index():
    return render_template('registration.html')

@app.route("/register", methods=['POST'])
def register():
    if not Register.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password'])
    }
    id = Register.save(data)
    session['registration_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = Register.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['registration_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'registration_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['registration_id']
    }
    return render_template("dashboard.html",registration=Register.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

