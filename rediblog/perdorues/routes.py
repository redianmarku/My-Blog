from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from rediblog import db, bcrypt
from rediblog.models import Perdorues, Postim
from rediblog.perdorues.forms import (FormRegjistrimi, FormHyrje, FormPerditsimi,
                                   RequestResetForm, NdryshoFjalkalimin)
from rediblog.perdorues.utils import save_picture, dergo_reset_email

perdorues = Blueprint('perdorues', __name__)


@perdorues.route("/regjistrohu", methods=['GET','POST'])
def regjistrohu():
    form = FormRegjistrimi()
    if current_user.is_authenticated:
        return redirect(url_for('main.kryefaqe'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        perdorues = Perdorues(emri_perdoruesit=form.emri_perdoruesit.data, email=form.email.data, password=hashed_password)
        db.session.add(perdorues)
        db.session.commit()
        flash('Adresa u krijua! Tani ti mund te hysh.', 'success')
        return redirect(url_for('perdorues.hyr'))
    return render_template('regjistrohu.html', title='Regjistrohu', form=form)


@perdorues.route("/hyr",  methods=['GET','POST'])
def hyr():
    form = FormHyrje()
    if current_user.is_authenticated:
        return redirect(url_for('main.kryefaqe'))
    if form.validate_on_submit():
        user = Perdorues.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.mbajmend.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.kryefaqe'))
        else:
            flash('Nuk munda te aksesoja adresen tende. Ju lumtem kontrolloni email ose fjalkalimin!', 'danger')
    return render_template('hyr.html', title='Hyr', form=form)


@perdorues.route("/dil")
def dil():
    logout_user()
    return redirect(url_for('main.kryefaqe'))


@perdorues.route("/llogaria",  methods=['GET','POST'])
@login_required
def llogaria():
    form = FormPerditsimi()
    if form.validate_on_submit():
        if form.foto.data:
            picture_file = save_picture(form.foto.data)
            current_user.image_file = picture_file
        current_user.emri_perdoruesit = form.emri_perdoruesit.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Llogaria juaj u perditsua!', 'success')
        return redirect(url_for('perdorues.llogaria'))
    elif request.method == 'GET':
        form.emri_perdoruesit.data = current_user.emri_perdoruesit
        form.email.data = current_user.email
    image_file = url_for('static', filename='imazhet_profilit/' + current_user.image_file)
    return render_template('llogaria.html', title='llogaria', image_file=image_file, form = form)


@perdorues.route("/user/<string:emri_perdoruesit>")
def perdorues_postim(emri_perdoruesit):
    page = request.args.get('page', 1, type=int)
    perdorues = Perdorues.query.filter_by(emri_perdoruesit=emri_perdoruesit).first_or_404()
    postime = Postim.query.filter_by(autori=perdorues).order_by(Postim.data_postimit.desc()).paginate(page=page, per_page=5)
    return render_template('perdorues_postim.html', postime=postime)

@perdorues.route("/ndrysho_fjalkalimin", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.kryefaqe'))
    form = RequestResetForm()
    if form.validate_on_submit():
        perdorues = Perdorues.query.filter_by(email=form.email.data).first()
        dergo_reset_email(perdorues)
        flash('U dergua nje email me instruksionet per te ndryshuar fjalkalimin tuaj.', 'info')
        return redirect(url_for('perdorues.hyr'))
    return render_template('reset_request.html', title='Ndrysho Fjalkalimin', form=form)


@perdorues.route("/ndrysho_fjalkalimin/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.kryefaqe'))
    user = Perdorues.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('perdorues.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('perdorues.hyr'))
    return render_template('reset_token.html', title='Reset Password', form=form)