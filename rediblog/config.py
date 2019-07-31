class Config:
	SECRET_KEY = 'celsisekret'
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@localhost/rediblog'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'redian0marku@gmail.com'
	MAIL_PASSWORD = 'markuredian16'