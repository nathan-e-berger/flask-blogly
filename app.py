"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db




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
    user_list = User.query.all()
    return render_template('user-list.html', user_list=user_list)

@app.get('/users/<int:id>')
def show_user():
    this_user = User.query.get(id)
    return render_template('user-page.html', user=this_user)

@app.get('/users/new')
def show_registration_form():
    return render_template('new-user.html')

@app.post('/users/new')
def register_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form.get("image_source")

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.get('/users/<int:id>/edit')
def show_edit():

@app.post('/users/<int:id>/edit')
def edit_user():


