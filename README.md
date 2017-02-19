[![Build Status](https://travis-ci.org/abbec/pantry.svg?branch=master)](https://travis-ci.org/abbec/pantry)
[![codecov](https://codecov.io/gh/abbec/pantry/branch/master/graph/badge.svg)](https://codecov.io/gh/abbec/pantry)
[![Code Health](https://landscape.io/github/abbec/pantry/master/landscape.svg?style=flat)](https://landscape.io/github/abbec/pantry/master)

# pantry
Pantry is a small service for leasing hardware from a pool

## Setting up
To get a development environment up and running, install all requirements with:

    $ pip install -r requirements.txt

This will install all requirements and pantry itself as an editable package. This is needed for unit tests to be able to find it.

## Seeding the database
There is a small utility script for creating and populating the database. Run it by typing:

    $ python manage.py seed

