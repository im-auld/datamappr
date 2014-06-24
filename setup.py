from setuptools import setup


long_description = """
A Flask app that receives datasets form a database via AJAX and uses a 
a javascript library to generate a heatmap overlay for a Google Map pane.
"""

setup(
    name="datamapper",
    version="0.1-dev",
    description="Data Heat Mapper",
    long_description=long_description,
    url='https://github.com/xbobo/FinalProject1',
    # Author details
    author='Ian Auld, Jack Tian, Chris',
    author_email='imauld@gmail.com',
    # Choose your license
    #   and remember to include the license text in a 'docs' directory.
    license='MIT',
    packages=['datamapper'],
    install_requires=[
                        'setuptools',
                        'Flask',
                        'Flask-WTF',
                        'Flask-SQLAlchemy',
                        'pytest'
                    ]
)