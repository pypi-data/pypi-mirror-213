from setuptools import setup

setup(
    name='Zevon',
    version='0.5.0',
    packages=['zevon'],
    description='Zevon - turn a API Gateway / Lambda event to a Flask thing',
    author='Chuck Muckamuck (obviously a pseudonym)',
    author_email='Chuck.Muckamuck@gmail.com',
    install_requires=[
        'Flask>=2.1',
        'Werkzeug<2.2.3'
    ]
)
