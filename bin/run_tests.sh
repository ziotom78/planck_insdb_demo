#!/bin/sh

black --exclude=migrations --check . && \
    flake8 --exclude=migrations --max-line-length=120 &&
    poetry run python3 manage.py test


