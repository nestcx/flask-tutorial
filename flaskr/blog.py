from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)

from wekzeug.excetions import abort

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



