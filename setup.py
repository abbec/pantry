from setuptools import setup

setup(name='pantry',
      version='0.1',
      packages=['pantry'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.5',
          ],
      install_requires=[
          'Flask',
          'Flask-SQLAlchemy',
          'Flask-Migrate',
          ])
