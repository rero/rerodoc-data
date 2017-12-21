# -*- coding: utf-8 -*-

"""rerodoc application factories."""

from flask import render_template
from lxml import etree


def dublin_core(pid, record, **kwargs):
    return etree.fromstring(render_template('rerodoc/oai_dc.html', record=record.get('_source')))