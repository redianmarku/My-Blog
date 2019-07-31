from flask import render_template, request, Blueprint
from rediblog.models import Postim

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/kryefaqe")
def kryefaqe():
    page = request.args.get('page', 1, type=int)
    postime = Postim.query.order_by(Postim.data_postimit.desc()).paginate(page=page, per_page=5)
    return render_template('kryefaqja.html', postime=postime)


@main.route("/rreth")
def rreth():
    return render_template('rrethnesh.html', titulli='Rreth Nesh')
