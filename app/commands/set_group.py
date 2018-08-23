import click
from flask import current_app, g, url_for
# g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request.
# current_app is another special object that points to the Flask application handling the request.

import os

from app.db import get_db

from flask.cli import with_appcontext


@click.command('set-group')
@click.argument('group_name')
@with_appcontext
def set_group_command(group_name):
    """Set group for the annotation."""

    db = get_db()

    groups = db.execute(
        'SELECT group_name'
        ' FROM groups'
    )

    images = db.execute(
        'SELECT image_url'
        ' FROM images'
    )

    images_in_db = []
    for group in images:
        images_in_db.append(group['image_url'])

    print(images_in_db)

    groups_in_db = []
    for group in groups:
        groups_in_db.append(group['group_name'])

    if group_name not in groups_in_db:
        click.echo('There is not a group with that name in the database.')
        click.echo('Failed to update.')
        click.echo('Available names:')
        for group in groups_in_db:
            click.echo(group)
        return

    db.execute(
        'UPDATE current_group SET current_group_name=?',
        (group_name,)
    )

    db.commit()
    
    click.echo('Successfully updated group for annotation.')


def set_group(app):
    app.cli.add_command(set_group_command)