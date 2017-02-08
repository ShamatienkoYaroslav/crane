from setuptools import setup, find_packages

setup(
    name="Crane",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'appdirs==1.4.0',
        'click==6.7',
        'docker==2.0.2',
        'docker-pycreds==0.2.1',
        'Flask==0.12',
        'itsdangerous==0.24',
        'Jinja2==2.9.5',
        'MarkupSafe==0.23',
        'packaging==16.8',
        'pyparsing==2.1.10',
        'requests==2.13.0',
        'six==1.10.0',
        'websocket-client==0.40.0',
        'Werkzeug==0.11.15'
],
    author="ShamatienkoYaroslav",
    author_email="shamatienko.yaroslav@gmail.com",
    description="App for manage docker container",
    long_description=open('README.md').read(),
    license="GPLv2+",
    url=""
)
