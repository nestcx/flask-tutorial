### Flaskr - Flask's Tutorial Application

Hosted on AWS Elastic Bean(EB): http://flask-env2.us-east-2.elasticbeanstalk.com/

Steps to host on EB:

- download and install EB CLI

- generate list of dependencies from the Python environment:

`pip freeze > REQUIREMENTS.txt`

Remove line referencing git repository and `pkg-resources==0.0.0` if present.

- create .ebignore file and add ignore relevant directories/files

## issue 1: 

## issue 2: Python Module Imports

In the tutorial by default, the application factory, create_app(), imports db.py, blog.py, and auth.py by using _relative_ imports:

`from . import db`

and refers to the modules by their name.

This will not work on EB. Solution:

`import flaskr.db`

flaskr is the package, as dictated by the presence of __init__.py, and db is a module within that package.

You must then refer to db as `flaskr.db`. 


