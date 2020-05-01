from setuptools import find_packages, setup

setup(
        name='flaskr',
        version='1.0.0',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'flask',
        ],
)

# packages tells Python what package directories / Python files to include.
# find_packages() finds these directories automatically so you don't have to type them out.. phew.

# to include other files such as static and template directories, include_package_data is set to true.
# Python will need another file named MANIFEST.in to tell what this other data is.
