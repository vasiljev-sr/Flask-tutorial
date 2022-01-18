from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import requests
import json
bp = Blueprint('bot', __name__ , url_prefix='/bot')


@bp.route('/last_pos', methods=(['GET']))
def last_pos():
    db = get_db()
    last_position = get_db().execute(
        'SELECT id, status, profit, margin,position_size,symbol,entry_price,opened_position, datetime '
        ' FROM positions p '
         'ORDER BY id DESC LIMIT 1'
    ).fetchone()

    # [last_position.pop(key) for key in ['id', 'datetime']]
    # data = json.dumps(last_position, indent=4, sort_keys=True, default=str)
    # requests.post('http://127.0.0.1:5000/bot/new_order', json=data)
    return last_position


@bp.route('/new_order', methods=('GET', 'POST'))
def new_order():
    if request.method == 'POST':
        data = json.loads(request.json)

        opened_position = data['opened_position']
        entry_price = data['entry_price']
        symbol = data['symbol']
        position_size = data['position_size']
        margin = data['margin']
        profit = data['profit']
        status = data['status']

        db = get_db()
        db.execute(
            'INSERT INTO positions (opened_position, entry_price, symbol, position_size,margin,profit,status)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?)',
            (opened_position, entry_price, symbol,position_size,margin,profit,status)
        )
        db.commit()
    return Response('Ok')








