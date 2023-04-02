from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.user import User

app.secret_key = "whatever you want"

@app.route("/")
def index():
    user = User.get_all()
    print(user)
    return render_template("show_all.html", users = user)

@app.route("/create")
def create():
    return render_template("create_user.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/create')
    data = {
        "id": request.form["id"],
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "created_at" : request.form["created_at"]
    }
    User.save(data)
    return redirect('/')

@app.route('/users')
def show_users():
    users=User.get_all()
    return render_template("show_all.html",users=users)

@app.route('/users/edit/<int:id>')
def edit(id):
    users=User.get_one(id)
    return render_template("edit.html", user=users)

@app.route('/users/update', methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/users')

@app.route('/users/show/<int:id>')
def show_one(id):
    users=User.get_one(id)
    print(users)
    return render_template("show_one.html", users=users)

@app.route('/users/delete/<int:id>')
def delete(id):
    User.delete(id)
    return redirect ('/users')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    return redirect('/dashboard')