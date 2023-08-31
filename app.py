"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db, Post
import datetime




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def start():
    """Redirect to list of users"""
    return redirect('/users')

@app.get('/users')
def show_all_users():
    """Show the list of all users."""
    user_list = User.query.all()
    return render_template('user-list.html', user_list=user_list)

@app.get('/users/<int:id>')
def show_user(id):
    """Show an individual user's page."""
    user = User.query.get_or_404(id)
    return render_template('user-page.html', user=user)

@app.get('/users/new')
def show_registration_form():
    """Show the form to register a new user."""
    return render_template('new-user.html')

@app.post('/users/new')
def register_user():
    """Handle form submission to add a new user to the database."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_source"] or None
    print("this is image_url", type(image_url))
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.get('/users/<int:id>/edit')
def show_edit(id):
    """Show a form to edit a user's page."""
    user = User.query.get_or_404(id)
    return render_template("edit-user.html", user=user)

@app.post('/users/<int:id>/edit')
def edit_user(id):
    """Handle form submission for edits to a user's page."""
    user = User.query.get_or_404(id)
    new_first = request.form["first_name"]
    new_last = request.form["last_name"]
    new_image = request.form["image_source"]
    if new_first:
        user.first_name = new_first
    if new_last:
        user.last_name = new_last
    if new_image:
        user.image_url = new_image

    db.session.commit()

    return redirect(f'/users/{id}')


@app.post('/users/<int:id>/delete')
def delete_user(id):
    """Handle form submission for clicking the delete button on a user page."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.get('/users/<int:id>/posts/new')
def show_new_post_form(id):
    """Show the form for making a new post"""
    user = User.query.get_or_404(id)
    return render_template('post-form.html', user=user)

@app.post('/users/<int:id>/posts/new')
def add_new_post(id):
    # user = User.query.get_or_404(id)
    post_title = request.form["post_title"]
    post_content = request.form["post_content"]
    created_at = datetime.datetime.now()
    post = Post(title=post_title, content=post_content, user_id=id, created_at=created_at)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{id}')

@app.get("/posts/<int:id>")
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template("post-page.html", post=post)

@app.get("/posts/<int:id>/edit")
def show_edit_post(id):
    post = Post.query.get_or_404(id)
    return render_template("edit-post.html", post=post)

@app.post("/posts/<int:id>/edit")
def update_post(id):
    post = Post.query.get_or_404(id)
    post_title = request.form["post_title"]
    post_content = request.form["post_content"]
    post.title=post_title
    post.content=post_content
    db.session.commit()
    return redirect(f"/posts/{id}")

