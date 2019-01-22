
from setuptools import setup

setup(
    name='junit2html',
    version='0.1',
    description='Generate html file from junit reports',
    author='Ahmed El-Sayed',
    author_email='ahmed.m.elsayed93@gmail.com',
    url='https://github.com/AhmedHanafy725/junit2html_plugin',
    install_requires=['jinja2'],
    # packages=['junit2html'],
    package_data = ['template.html'],
    include_package_data=True,
    entry_points = {
        'nose.plugins.0.10': ['junit2html = junit2html:Junit2Html']
        },
    )