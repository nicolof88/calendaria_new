from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo
from app import db
from app.models import User

# Form to login
class LoginForm(FlaskForm):
    email = StringField('Email', 
    	validators=[DataRequired(), Email('Enter a valid email address')], 
    	render_kw={"placeholder": "email", 
            "class": "form-control"})

    password = PasswordField('Password', 
    	validators=[DataRequired()],
    	render_kw={"placeholder": "password", 
            "class": "form-control"})

    remember_me = BooleanField('Remember me',
    	render_kw={"class": "form-check-input", 
            "type": "checkbox", 
            "id": "remember_me"})
    # submit = SubmitField('Sign In', render_kw={"class": "btn btn-link text-center"})


# Form to register a new user
class RegistrationForm(FlaskForm):
	email = StringField('Email address', 
    	validators=[DataRequired(), Email('Enter a valid email address')], 
    	render_kw={"placeholder": "email", 
            "class": "form-control", 
            "id": "register-email"})

	dob = DateField('Date of Birth',
		validators=[DataRequired()],
		render_kw={"class": "form-control", 
            "id": "register-bday", 
            "placeholder": "mm/dd/yyyy", 
            "onkeypress": "return false"},
		format="%m/%d/%Y")

	first_name = StringField('First name', 
    	validators=[DataRequired()], 
    	render_kw={"placeholder": "first name", 
            "class": "form-control", 
            "id": "register-fname"})

	password = PasswordField('Set your password', 
    	validators=[DataRequired()],
    	render_kw={"placeholder": "password", 
            "class": "form-control", 
            "id": "register-pword"})

	password2 = PasswordField('Repeat password', 
    	validators=[DataRequired(), EqualTo('password')],
    	render_kw={"placeholder": "repeat password", 
            "class": "form-control", 
            "id": "register-pword2"})

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('An account with that email already exists.')


# Update the profile information (no password yet)
class UpdateProfileForm(FlaskForm):
    email = StringField('Email address', 
        validators=[DataRequired(), Email('Enter a valid email address')], 
        render_kw={"placeholder": "email", 
            "class": "form-control", 
            "id": "update-email"})

    dob = DateField('Date of Birth',
        validators=[DataRequired()],
        render_kw={"class": "form-control", 
            "id": "update-bday", 
            "placeholder": "mm/dd/yyyy", 
            "onkeypress": "return false"},
        format="%m/%d/%Y")

    first_name = StringField('First name', 
        validators=[DataRequired()], 
        render_kw={"placeholder": "first name", 
            "class": "form-control", 
            "id": "update-fname"})