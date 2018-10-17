from flask_mail import Message
from flask import render_template
from app import app, mail
from threading import Thread

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	# mail.send(msg)
	Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user, loc):
	if loc == 'es':
		title = '[Calendaria] Actualice su contrasena'
		email_txt_temp = 'es/email/reset_password.txt'
		email_html_temp = 'es/email/reset_password.html'
	else:
		title = '[Calendaria] Reset your password'
		email_txt_temp = 'email/reset_password.txt'
		email_html_temp = 'email/reset_password.html'
		
	token = user.get_reset_password_token()
	send_email(title, 
		sender=app.config['ADMINS'][0],
		recipients=[user.email],
		text_body=render_template(email_txt_temp, user=user, token=token),
		html_body=render_template(email_html_temp, user=user, token=token))
