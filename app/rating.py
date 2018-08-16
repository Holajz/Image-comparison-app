from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('rating', __name__)



@bp.route('/sortable1', methods=['GET'])
@login_required
def sortable1():
    db = get_db()
    images = db.execute(
        'SELECT *'
        ' FROM images'
        ' WHERE images.group_status IN'
        '   (SELECT group_status'
        '       FROM images'
        '       ORDER BY RANDOM()'
        '       LIMIT 1)'
        ' ORDER BY RANDOM()'
        ' LIMIT 6'
    )
    return render_template('rating/sortable.html', images=images)

    images = db.execute(

    )

@bp.route('/sortable1', methods=['POST'])
@login_required
def sortable11():
    if request.form['ratings']:
        ratings = request.form['ratings']
        int_ratings = [int(i) for i in ratings.split()]

        db = get_db()
        message = None

        db.execute(
            'INSERT INTO rating (rated_first, rated_second, rated_third, rated_forth, rated_fifth, rated_sixth, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (int_ratings[0], int_ratings[1], int_ratings[2], int_ratings[3], int_ratings[4], int_ratings[5], g.user['id'])
        )
        db.commit()

        message = "Successfully rated images, here is some more cats for you to rate."
        flash(message)

        return redirect(url_for('rating.sortable1'))




@bp.route("/sortable2", methods=['GET'])
@login_required
def sortable2():
    db = get_db()
    images = db.execute(
        'SELECT *'
        ' FROM images'
        ' WHERE images.group_status IN'
        '   (SELECT group_status'
        '       FROM images'
        '       ORDER BY RANDOM()'
        '       LIMIT 1)'
        ' ORDER BY RANDOM()'
        ' LIMIT 6'
    )
    return render_template("rating/sortable2.html", images=images)


@bp.route("/sortable2", methods=['POST'])
@login_required
def sortable22():
    if request.form['ratings'] and request.form['type']:
        if request.form['type'] == 'sortable':
            ratings = request.form['ratings']
            int_ratings = [int(i) for i in ratings.split()]

            db = get_db()
            message = None

            db.execute(
                'INSERT INTO rating (rated_first, rated_second, rated_third, rated_forth, rated_fifth, rated_sixth, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (int_ratings[0], int_ratings[1], int_ratings[2], int_ratings[3], int_ratings[4], int_ratings[5], g.user['id'])
            )
            db.commit()
            # last_id = db.last_insert_rowid()

            message = "Successfully rated images, here is some more cats for you to rate."
            flash(message)

            return redirect(url_for('rating.sortable2'))
        elif request.form['type'] == 'select':
            ratings = request.form['ratings']
            int_ratings = [int(i) for i in ratings.split()]

            db = get_db()
            message = None

            db.execute(
                'INSERT INTO selection (rated_first, rated_second, author_id) VALUES (?, ?, ?)',
                (int_ratings[0], int_ratings[1], g.user['id'])
            )
            db.commit()

            message = "Successfully rated images, here is some more cats for you to rate."
            flash(message)

            return redirect(url_for('rating.sortable2'))
        else:
            ratings = request.form['ratings']
            int_ratings = [int(i) for i in ratings.split()]
            amount = request.form['amount']

            db = get_db()
            message = None

            db.execute(
                'INSERT INTO amount (image_rated, rating, author_id) VALUES (?, ?, ?)',
                (int_ratings[0], amount, g.user['id'])
            )
            db.commit()

            message = "Successfully rated images, here is some more cats for you to rate."
            flash(message)

            return redirect(url_for('rating.sortable2'))
    
    return redirect(url_for('rating.sortable2'))


@login_required
@bp.route("/sortable3", methods=['GET'])
def sortable3():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        # db = get_db()
        # posts = db.execute(
        #     'SELECT p.id, title, body, created, author_id, username'
        #     ' FROM post p JOIN user u ON p.author_id = u.id'
        #     ' ORDER BY created DESC'
        # ).fetchall()

        # SELECT name
        #     FROM random AS r1 JOIN
        #    (SELECT CEIL(RAND() *
        #                  (SELECT MAX(id)
        #                     FROM random)) AS id)
        #     AS r2
        # WHERE r1.id >= r2.id
        # ORDER BY r1.id ASC
        # LIMIT 1
        pass
    return render_template("rating/sortable3.html")