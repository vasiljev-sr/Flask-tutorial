from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    order = db.execute(
        'SELECT p.id, p.datetime, opened_position, entry_price,'
        ' position_size, margin, profit, status ,symbol '
        ' FROM positions p JOIN current_position u ON p.id = u.id'

    ).fetchone()
    settings = db.execute(
        'SELECT *'
        ' FROM bot_settings '
    ).fetchone()
    return render_template('blog/index.html', order=order, settings=settings)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/history')
@login_required
def history():
    db = get_db()
    orders = get_db().execute(
        'SELECT id, status, profit, margin,position_size,symbol,entry_price,opened_position, datetime '
        'FROM positions p '
        'ORDER BY id DESC'
    ).fetchall()
    return render_template('blog/positions.html', orders=orders)


@bp.route('/history/<int:id>')
@login_required
def position_history(id):

    position = get_db().execute(
        'SELECT id, datetime, operation, amount, price'
        ' FROM order_history p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchall()
    if len(position) == 0:
        abort(404, f"Position id {id} doesn't exist.")

    return render_template('blog/position_history.html', position=position)