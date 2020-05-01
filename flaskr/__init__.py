# __init.py__ serves double duty
#  1) tell's Python the flaskr directory is a package
#  2) it will contain the application factory

import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    print("name: " + __name__)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
            )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello/')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    # by default, the index view defined in blog.py is available at blog.index
    # app.add_url_rule associates the endpoint name 'index' with the '/' url, such that ...
    # url_for('blog.index') and url_for('index') both generate '/'
    app.add_url_rule('/', endpoint='index') 

    return app
