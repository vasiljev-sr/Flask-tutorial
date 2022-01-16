from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('bot', __name__)


@bp.route('/order', methods=('GET', 'POST'))
def order():
    last_position = get_db().execute(
        'SELECT *'
        ' FROM positions'
        'ORDER BY id DESC LIMIT 1'
    ).fetchone()
    return render_template('bot/order.html', last_position=last_position)


def get_last_position():
    db = get_db()
    last_position = get_db().execute(
        'SELECT *'
        ' FROM positions'
         'ORDER BY id DESC LIMIT 1'
    ).fetchone()





