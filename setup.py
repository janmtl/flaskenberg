from setuptools import setup, find_packages

setup(
    name="flaskenberg",
    version="0.1",
    packages=find_packages(),
    scripts = ['scripts/runserver.py'],
    zip_safe=False,
    install_requires=['Flask'],
)