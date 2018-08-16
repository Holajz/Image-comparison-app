import re
from datetime import datetime

from flask import (Blueprint, Flask, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify

from app.auth import admin_required, bp, login_required
from app.db import get_db

from . import app, auth

import json


@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/home", methods=['GET'])
def home_home():
    return render_template("home.html")

@app.route("/information", methods=['GET'])
def information():
    return render_template("information.html")


@app.route("/contact", methods=['GET'])
def contact():
    return render_template("contact.html")


@app.route("/api/rating/<num_of_ratings>", methods=['GET'])
@login_required
@admin_required
def get_data(num_of_ratings):
    """Get number of rating data of /api/rating/<number_of_ratings>
    """
    db = get_db()
    num = str(num_of_ratings)


    ratings = db.execute(
        'SELECT *'
        ' FROM rating'
        ' WHERE id IN'
        '   (SELECT id'
        '    FROM rating'
        '    ORDER BY RANDOM()'
        '    LIMIT ?)', [num] 
    ).fetchall()

    all_ratings = list()
    for rating in ratings:
        all_ratings.append(list(rating))

    return jsonify(all_ratings)


@app.route("/api/rating/<group_name>/<num_of_ratings>", methods=['GET'])
@login_required
@admin_required
def get_group_ratings(group_name, num_of_ratings):
    """Get number of rating data for the given group /api/rating/<group_name>/<num_of_ratings>
    """
    db = get_db()
    num = str(num_of_ratings)
    group = str(group_name)


    ratings = db.execute(
        'SELECT DISTINCT rating.rated_first, rating.rated_second, rating.rated_third, rating.rated_forth, rating.rated_fifth, rating.rated_sixth'
        ' FROM rating'
        ' INNER JOIN images'
        ' ON images.group_status = ?'
        ' LIMIT ?', (group, num)
    ).fetchall()

    all_ratings = list()
    for rating in ratings:
        all_ratings.append(list(rating))

    return jsonify(all_ratings)


@app.route("/api/rating/id/<image_id>", methods=['GET'])
@login_required
@admin_required
def get_image_ratings(image_id):
    db = get_db()
    num = str(image_id)


    rating = db.execute(
        'SELECT rating.rated_first, rating.rated_second, rating.rated_third, rating.rated_forth, rating.rated_fifth, rating.rated_sixth'
        ' FROM rating'
        ' WHERE rating.rated_first = ? OR rating.rated_second = ? OR rating.rated_third = ? OR rating.rated_forth = ? OR rating.rated_fifth = ? OR rating.rated_sixth = ?', [image_id, image_id, image_id, image_id, image_id, image_id]
    ).fetchall()

    selection = db.execute(
        'SELECT selection.rated_first, selection.rated_second'
        ' FROM selection'
        ' WHERE selection.rated_first = ? OR selection.rated_second = ?', [image_id, image_id]
    ).fetchall()

    all_ratings = list()
    for rating in rating:
        all_ratings.append(list(rating))
    for select in selection:
        all_ratings.append(list(select))

    compared_with = list()
    for rating in all_ratings:
        for el in rating:
            if el not in compared_with and el != int(num):
                compared_with.append(el)
    compared_with = set(compared_with)


    content = dict()

    for compare in compared_with:
        content[compare] = {"better" : 0, "worse" : 0}

    for rating in all_ratings:
        occurences = compared_with.intersection(rating)
        for occurence in occurences:
            index_occurence = rating.index(occurence)
            index_num = rating.index(int(num))

            if index_num > index_occurence:
                content[occurence]["worse"] += index_num - index_occurence
            else:
                content[occurence]["better"] += index_occurence - index_num
    
    
    final_dict = dict()
    final_dict["image_id"] = int(num)
    final_dict["compared_with"] = list(compared_with)
    final_dict["when_compared_with"] = content

    return jsonify(final_dict)

## TODO ##
# podle neuronovky zobrazovat obrazku - nenahodne
# hourglass model
# resnet
# siamske neuronove site, na vstupu 
