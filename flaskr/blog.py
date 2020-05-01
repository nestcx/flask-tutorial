from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

# login_required checks if g.user is set
from flaskr.auth import login_required

from flaskr.db import get_db

# this is all that is needed to be able to register a blueprint in the factory as blog.bp
# the auth blueprint had a third argument, a url_prefix: url_prefix='/blog'
# since it has no url prefix, the index for for instance, will be at '/'...
# and the create view will be at /create, etc.
# rationale: 'the blog is the main feature of Flaskr, so it makes sense that the blog index will be the main 'index'
# in the factory, need to add a few URL rules: see __init__.py
bp = Blueprint('blog', __name__)

# is this linked to the rule defined in the factory?
# where '/' corresponds to the endpoint 'index'?
# in auth, maybe this wasn't necessary because the route matched the view function name.
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u on p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()
    return render_template('blog/index.html', posts=posts)

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
            db.execute('INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)', (title, body, g.user['id']))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

# this function serves a purpose for both the update and delete views,
# which need to fetch a post by id and check if the author matches the
# logged in user
# this function can also be used to get a post without checking the author,
# such as in displaying an individual post.
def get_post(id, check_author=True):
    post = get_db().execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?', (id,)).fetchone()

    if post is None:
        # abort will raise a special exception which returns a HTTP status code
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

# this is the first view that has taken an argument - id
# the argumet in update(id) corresponds to <int:id> in the route
# real url:    /1/update
# flask captures the 1, makes sure it's an int, passes it to the id argument.
# by not specifying int, it will be a string.
@bp.route('/<int:id>/update', methods('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':

        # get the values from the form
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
    
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(UPDATE post SET title = ?, body = ? WHERE id = ?, (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# in order to generate a URL to an update page, such as 1/update, url_for needs an ID
#     url_for('blogupdate', id=post['id'])
# - see this in index.html 







