from app import app, db, moment
from app.models import User
from flask import render_template, flash, redirect, url_for, request, g
from app.forms import (LoginForm, LoginESForm, RegistrationForm, RegistrationESForm, UpdateProfileForm, 
	UpdateProfileESForm, ResetPasswordForm, ResetPasswordESForm, 
	ResetPasswordRequestForm, ResetPasswordRequestESForm)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.util import date_utils
from app.email import send_password_reset_email
from datetime import datetime, timedelta, date
from flask_babel import get_locale
import locale


# Entry point, index
@app.route('/')
@app.route('/index')
@login_required
def index():
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'es':
		return redirect(url_for('index_es'))
	title = current_user.first_name + " Home"
	locale.setlocale(locale.LC_TIME, loc)
	dates = {}
	dates['today'] = date.today()
	dates['days_alive'] = date_utils.day_diff(dates['today'], current_user.dob.date())
	dates['round'] = date_utils.round_nbr(dates['today'])
	dates['quad'] = date_utils.quadrant(dates['today'])
	grid = date_utils.round_vals_from_date(date.today())
	return render_template('index.html', title=title, dates=dates, grid=grid)


# Spanish index
@app.route('/es')
@app.route('/es/index')
@login_required
def index_es():
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'en':
		return redirect(url_for('index'))
	title = current_user.first_name + " Home"
	locale.setlocale(locale.LC_TIME, loc)
	dates = {}
	dates = {}
	dates['today'] = date.today()
	dates['days_alive'] = date_utils.day_diff(dates['today'], current_user.dob.date())
	dates['round'] = date_utils.round_nbr(dates['today'])
	dates['quad'] = date_utils.quadrant(dates['today'])
	grid = date_utils.round_vals_from_date(date.today())
	return render_template('es/index.html', title=title, dates=dates, grid=grid)


# Login to the website
@app.route('/login', methods=['GET', 'POST'])
def login():
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'es':
		return redirect(url_for('login_es'))
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


# Login to the website in spanish
@app.route('/es/login', methods=['GET', 'POST'])
def login_es():
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'en':
		return redirect(url_for('login'))
	if current_user.is_authenticated:
		return redirect(url_for('index_es'))
	form = LoginESForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Email o contrasena invalidos. Por favor intente de nuevo')
			return redirect(url_for('login_es'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index_es')
		return redirect(next_page)
	return render_template('es/login.html', title="Ingresar", form=form)


# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'es':
		return redirect(url_for('register_es'))
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
	return render_template('register.html', title="Registration", form=form, loc=loc)


# Register a new user spanish
@app.route('/es/register', methods=['GET', 'POST'])
def register_es():
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'en':
		return redirect(url_for('register'))
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationESForm()
	if form.validate_on_submit():
		new_user = User(email=form.email.data, first_name=form.first_name.data, dob=form.dob.data)
		new_user.set_password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Ud. ha sido registrado correctamente.')
		return redirect(url_for('login'))
	return render_template('es/register.html', title="Crear nueva cuenta", form=form, loc=loc)


# Profile view
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'es':
		return redirect(url_for('profile_es', user_id=current_user.id))
	title = current_user.first_name.capitalize() + " Profile"
	user = User.query.get(user_id)
	return render_template('profile.html', title=title, user=user)


# Profile view spanish
@app.route('/es/profile/<int:user_id>')
@login_required
def profile_es(user_id):
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'en':
		return redirect(url_for('profile', user_id=current_user.id))
	title = current_user.first_name.capitalize() + " Perfil"
	user = User.query.get(user_id)
	return render_template('es/profile.html', title=title, user=user)



# Update profile
@app.route('/profile/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'es':
		return redirect(url_for('profile_es', user_id=current_user.id))
	title = current_user.first_name + "Update Profile"
	form = UpdateProfileForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.email = form.email.data
		current_user.dob = form.dob.data
		db.session.commit()
		return redirect(url_for('profile', user_id=current_user.id))
	return render_template('update.html', title=title, form=form)


# Update profile spanish
@app.route('/es/profile/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_es(user_id):
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'en':
		return redirect(url_for('profile', user_id=current_user.id))
	title = current_user.first_name + "Actualizar Perfil"
	form = UpdateProfileESForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.email = form.email.data
		current_user.dob = form.dob.data
		db.session.commit()
		return redirect(url_for('profile', user_id=current_user.id))
	return render_template('es/update.html', title=title, form=form)


# Log users out by re-directing them to Login
@app.route('/logout')
def logout():
	logout_user()
	loc = 'es'
	if loc == 'en':
		flash('You have been successfully logged out.')
	else:
		flash('Ud. ha terminado la sesion.')
	return redirect(url_for('login'))


# Password change (required data)
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('index'))
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'es':
		return redirect(url_for('reset_password_request_es'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password')
		return redirect(url_for('login'))
	return render_template('reset_password_request.html', title='Reset Password', form=form)


# Password change (required data)
@app.route('/es/reset_password_request', methods=['GET', 'POST'])
def reset_password_request_es():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('index'))
	# loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	loc = 'es'
	if loc == 'en':
		return redirect(url_for('reset_password_request'))
	form = ResetPasswordRequestESForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user, loc)
		flash('Se han enviado instrucciones a su correo para actualizar la contrasena.')
		return redirect(url_for('login'))
	return render_template('es/reset_password_request.html', title='Actualizar Contrasena', form=form)


# Reset password view
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)


# Reset password view
@app.route('/es/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_es(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordESForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Su contrasena ha sido actualizada.')
		return redirect(url_for('login'))
	return render_template('es/reset_password.html', form=form)


# Test view
@app.route('/test_date')
def test_date():
	utc_date = datetime.utcnow()
	moment_date = moment.create(utc_date)
	return render_template('test_date.html', utc_date=utc_date, moment_date=moment_date)

# Test view
@app.route('/test_locale')
def test_locale():
	loc = request.accept_languages.best_match(app.config['LANGUAGES'])
	babel_loc = str(get_locale())
	return render_template('test_locale.html', loc=loc, babel_loc=babel_loc)
