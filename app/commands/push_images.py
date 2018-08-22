import click
from flask import current_app, g, url_for

import fnmatch
import re

import os

from app.db import get_db

from flask.cli import with_appcontext



@click.command('update-images')
@click.argument('images_folder')
@with_appcontext
def update_images_command(images_folder):
    """Recursively go through image folder and add every image to the database.
       First level of folders are groups
    """
    
    db = get_db()
    folder = os.path.join(current_app.static_folder, images_folder)

    folder = folder.rstrip(os.path.sep)

    first_level_dirs = []
    for dirpath, dirs, files in os.walk(folder):
        first_level_dirs = dirs
        break
    
    groups = db.execute(
        'SELECT group_name'
        ' FROM groups'
    )

    groups_in_db = []

    for group in groups:
        groups_in_db.append(group['group_name'])

    new_groups = set(first_level_dirs).difference(groups_in_db)

    includes = ['*.jpg', '*.png', '*.jpeg', '*.bmp']
    includes = r'|'.join([fnmatch.translate(x) for x in includes])

    for group in new_groups:
        db.execute(
            'INSERT INTO groups (group_name) VALUES (?)',
            [group]
        )

        for root, dirs, files in os.walk(os.path.join(folder, group)):
            files = [os.path.join(root, f) for f in files]
            files = [os.path.relpath(f, current_app.static_folder).replace("\\","/") for f in files]
            files = [f for f in files if re.match(includes, f)]

            for fname in files:
                db.execute(
                    'INSERT INTO images (image_url, group_status) VALUES (?, ?)',
                    (fname, group)
                )
    db.commit()

    if new_groups:
        click.echo('Successfully updated images and groups.')
        click.echo('Added groups:')
        click.echo(new_groups)
    else:
        click.echo('There were no new groups found.')




def init_images(app):
    app.cli.add_command(update_images_command)