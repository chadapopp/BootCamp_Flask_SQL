from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.post import Post
from flask_app.controllers import users

@app.route('/posts', methods = ["POST"])
def create_post():
    if not Post.validate_post(request.form):
        return redirect('/wall')
    Post.save(request.form)
    return redirect('/wall')

@app.route('/posts/delete/<post_id>')
def delete_post(post_id):
    Post.delete(post_id)
    return redirect('/wall')