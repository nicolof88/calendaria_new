from app import app, db
from app.models import User
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, UpdateProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from .util import date_utils
from datetime import timedelta, date


# Entry point
@app.route('/')
@app.route('/index')
@login_required
def index():
	title = current_user.first_name + " Home"
	dates = {}
	dates['today'] = date.today()
	dates['days_alive'] = date_utils.day_diff(dates['today'], current_user.dob.date())
	dates['quad'] = date_utils.quadrant(dates['today'])
	dates['round'] = date_utils.round_nbr(dates['today'])
	grid = date_utils.round_vals_from_date(date.today())
	print(grid['dates_str'])
	return render_template('index.html', title=title, dates=dates, grid=grid)


# Login to the website
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password. Please try again')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title="Login", form=form)


# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		new_user = User(email=form.email.data, first_name=form.first_name.data, dob=form.dob.data)
		new_user.set_password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Registration successfull! You can now log in')
		return redirect(url_for('login'))
	return render_template('register.html', title="Registration", form=form)


# Profile view
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
	title = current_user.first_name.capitalize() + " Profile"
	user = User.query.get(user_id)
	return render_template('profile.html', title=title, user=user)


# Update profile
@app.route('/profile/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
	title = current_user.first_name + "Update Profile"
	form = UpdateProfileForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.email = form.email.data
		current_user.dob = form.dob.data
		db.session.commit()
		return redirect(url_for('profile', user_id=current_user.id))
	return render_template('update.html', title=title, form=form)


# Log users out by re-directing them to Login
@app.route('/logout')
def logout():
	logout_user()
	flash('You have been successfully logged out.')
	return redirect(url_for('login'))