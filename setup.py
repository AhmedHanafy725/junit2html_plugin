
from setuptools import setup, find_packages

setup(
    name='junit2html',
    version='0.1',
    description='Generate html file for nosetests report',
    author='Ahmed Hanafy',
    author_email='ahmed.hanafy725@gmail.com',
    url='https://github.com/AhmedHanafy725/junit2html_plugin',
    install_requires=['jinja2'],
    py_modules=['junit2html/junit2html'],
    packages=['junit2html'],
    package_data = {'junit2html': ['template.html']},
    include_package_data=True,
    entry_points = {
        'nose.plugins.0.10': ['junit2html=junit2html.junit2html:Junit2Html']
        },
    )