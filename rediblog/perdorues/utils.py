
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from rediblog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/imazhet_profilit', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def dergo_reset_email(perdorues):
    token = perdorues.get_reset_token()
    msg = Message('Kerkesa per Ndryshimin e Fjalkalimit', sender='redian0marku@gmail.com', recipients=[perdorues.email])
    msg.body = f''' Per te ndryshuar fjalkalimin, shtypni linkun me poshte:
    {url_for('perdorues.reset_token', token=token, _external=True)}

    Nese ju nuk e keni bere kete kerkese ju lutem shperfilleni kete email dhe nuk do te ndodhe asnje ndryshim.

'''

    mail.send(msg)
