from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from rediblog.models import Perdorues

class FormRegjistrimi(FlaskForm):
	emri_perdoruesit = StringField('Emri i perdoruesit', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Fjalkalimi', validators=[DataRequired(), ])
	konfirmo_password = PasswordField('Konfirmo Fjalkalimin', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Regjistrohu')

	def validate_emri_perdoruesit(self, emri_perdoruesit):
		emri_perdoruesit = Perdorues.query.filter_by(emri_perdoruesit=emri_perdoruesit.data).first()
		if emri_perdoruesit:
			raise ValidationError('Ky emer eshte perdorur me pare. Ju lutem zgjidhni nje tjeter.')

	def validate_email(self, email):
		user = Perdorues.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Ky email eshte perdorur me pare. Ju lutem zgjidhni nje tjeter.')


class FormHyrje(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Fjalkalimi', validators=[DataRequired(), ])
	mbajmend = BooleanField('Mbaj mend')
	submit = SubmitField('Hyr')



class FormPerditsimi(FlaskForm):
	emri_perdoruesit = StringField('Emri i perdoruesit', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	foto = FileField('Perditso foton e profilit', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Ruaj Ndryshimet')

	def validate_emri_perdoruesit(self, emri_perdoruesit):
		if emri_perdoruesit.data != current_user.emri_perdoruesit:
		    emri_perdoruesit = Perdorues.query.filter_by(emri_perdoruesit=emri_perdoruesit.data).first()
		    if emri_perdoruesit:
			    raise ValidationError('Ky emer eshte perdorur me pare. Ju lutem zgjidhni nje tjeter.')

	def validate_email(self, email):
		if email.data != current_user.email:
		    user = Perdorues.query.filter_by(email=email.data).first()
		    if user:
			    raise ValidationError('Ky email eshte perdorur me pare. Ju lutem zgjidhni nje tjeter.')


class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Ndrysho Fjalkalimin')

	def validate_email(self, email):
		user = Perdorues.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Nuk ekziston nje llogari me kete email. Si fillim duhet te regjistrohesh.')


class NdryshoFjalkalimin(FlaskForm):
	password = PasswordField('Fjalkalimi', validators=[DataRequired(), ])
	konfirmo_password = PasswordField('Konfirmo Fjalkalimin', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Ndrysho Fjalkalimin')

		