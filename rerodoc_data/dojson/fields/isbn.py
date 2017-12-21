"""MARC 21 model definition."""

import re

from dojson import utils

from ..models import book, book2marc

ISBN10_REGEX = re.compile(r'^[0-9]{1,5}-[0-9]{1,7}-[0-9]{1,7}-[0-9,X]{1}$')
ISBN13_REGEX = re.compile(r'^[0-9]{13}$')


@book.over('isbn10', '^020..')
@utils.ignore_value
def isbn10(self, key, value):
    """Other Standard Identifier."""
    isbn = value.get('a')
    if ISBN13_REGEX.match(isbn):
        self['isbn13'] = isbn

    if ISBN10_REGEX.match(isbn):
        return isbn
    return None


@book2marc.over('020__', 'isbn10|isbn13')
def isbn102marc(self, key, value):
    """Other Standard Identifier."""
    return {
        'a': value
    }
