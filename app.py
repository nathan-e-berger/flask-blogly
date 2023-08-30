"""Blogly application."""

import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def start():
    """Redirect to list of users"""

