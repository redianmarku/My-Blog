from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from rediblog import db
from rediblog.models import Postim
from rediblog.postim.forms import FormPostimi

postimi = Blueprint('postim', __name__)


@postimi.route("/postim/new", methods=['GET','POST'])
@login_required
def new_postim():
    form = FormPostimi()
    if form.validate_on_submit():
        postim = Postim(titull = form.titulli.data, permbajtja = form.permbajtja.data, autori= current_user) 
        db.session.add(postim)
        db.session.commit()
        flash('Postimi juaj u krijua!', 'success')
        return redirect(url_for('main.kryefaqe'))
    return render_template('krijo_postim.html', title='Posim i ri', form=form, legend='Postim i ri')


@postimi.route("/postim/<int:postim_id>")
def postim(postim_id):
    postim = Postim.query.get_or_404(postim_id)
    return render_template('postim.html', title='postim.titull', postim=postim)



@postimi.route("/postim/<int:postim_id>/perditso", methods=['GET', 'POST'])
@login_required
def perditso_postim(postim_id):
    postim = Postim.query.get_or_404(postim_id)
    if postim.autori != current_user:
        abort(403)
    form = FormPostimi()
    if form.validate_on_submit():
        postim.titull = form.titulli.data
        postim.permbajtja = form.permbajtja.data
        db.session.commit()
        flash('Postimi juaj eshte perditesuar!', 'success')
        return redirect(url_for('postim.postim', postim_id=postim.id))
    elif request.method =='GET':
        form.titulli.data = postim.titull
        form.permbajtja.data = postim.permbajtja
    return render_template('krijo_postim.html', title= 'Perditso Postim', form=form, legend= 'Perditso postimin')


@postimi.route("/postim/<int:postim_id>/fshij", methods=['POST'])
@login_required
def fshij_postimin(postim_id):
    postim = Postim.query.get_or_404(postim_id)
    if postim.autori != current_user:
        abort(403)
    db.session.delete(postim)
    db.session.commit()
    flash('Postimi juaj u fshij!', 'success')
    return redirect(url_for('main.kryefaqe'))
