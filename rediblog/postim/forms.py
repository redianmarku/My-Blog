from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class FormPostimi(FlaskForm):
	titulli = StringField('Titulli', validators=[DataRequired()])
	permbajtja = TextAreaField('Permbajtja', validators=[DataRequired()])
	submit = SubmitField('Posto')
