
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from rediblog.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'perdorues.hyr'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Ju duhet te hyni ne llogarine tuaj per te pasur akses ne kete faqe!'
mail = Mail()


def krijo_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from rediblog.perdorues.routes import perdorues
	from rediblog.postim.routes import postimi
	from rediblog.main.routes import main
	from rediblog.errors.handlers import errors

	app.register_blueprint(perdorues)
	app.register_blueprint(postimi)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app




