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
    data = get_db().execute(
        'SELECT id, status, profit, margin,position_size,symbol,entry_price,opened_position, datetime '
        ' FROM positions p '
         'ORDER BY id DESC LIMIT 1'
    ).fetchone()

    # [last_position.pop(key) for key in ['id', 'datetime']]
    data = json.dumps(data, indent=4, sort_keys=True, default=str)

    # requests.post('http://127.0.0.1:5000/bot/new_order', json=data)
    return data


@bp.route('/new_pos', methods=('GET', 'POST'))
def new_pos():
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


@bp.route('/update_pos', methods=('GET', 'POST'))
def update_pos():
    if request.method == 'POST':
        data = json.loads(request.json)

        id = data['id']
        profit = data['profit']
        status = data['status']

        db = get_db()
        db.execute(
            'UPDATE positions SET profit = ?, status = ?'
            ' WHERE id = ?',
            (profit, status, id)
        )
        db.commit()
    return Response('Ok')


@bp.route('/current_pos', methods=('GET', 'POST'))
def current_pos():
    if request.method == 'POST':
        data = json.loads(request.json)

        id = data['id']
        datetime = data['datetime']

        db = get_db()
        db.execute(
            'UPDATE current_position SET id = ?, datetime = ?',
            (id,datetime )
        )
        db.commit()
    return Response('Ok')


@bp.route('/pos_history', methods=('GET', 'POST'))
def pos_history():
    if request.method == 'POST':
        data = json.loads(request.json)

        id = data['id']
        datetime = data['datetime']
        operation = data['operation']
        amount = data['amount']
        price = data['price']

        db = get_db()
        db.execute(
             'INSERT INTO order_history (id, datetime, operation, amount, price )'
            ' VALUES (?, ?, ?, ?, ?, ?, ?)',
            (id, datetime, operation, amount, price)
        )
        db.commit()
    return Response('Ok')


@bp.route('/settings', methods=('GET', 'POST'))
def settings():
    db = get_db()
    settings = db.execute(
        'SELECT *'
        ' FROM bot_settings '
    ).fetchone()

    data = json.dumps(settings, indent=4, sort_keys=True, default=str)

    return data














