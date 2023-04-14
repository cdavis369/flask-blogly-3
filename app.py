"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import User, db, connect_db
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

with app.app_context():
  connect_db(app)
  db.create_all()
  
@app.route('/')
def index():
  """ Redirect to users list """
  return redirect('/users')
  
@app.route('/users')
def users_list():
  """ Shows list of all users in db """
  users = User.query.order_by(User.last_name, User.first_name)
  return render_template("index.html", users=users)

@app.route('/users/new')
def new_user_form():
  """ Shows new user form for submission"""
  return render_template("user_form.html")

@app.route('/users/new', methods=["POST"])
def create_user():
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  image_url = request.form['image_url']
  
  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
  user = User.query.get(user_id)
  return render_template("user.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_view(user_id):
  user = User.query.get(user_id)
  return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
  user = User.query.get(user_id)
  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url']
  db.session.commit()
  return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
  User.query.filter_by(id=user_id).delete()
  db.session.commit()
  return redirect('/users')