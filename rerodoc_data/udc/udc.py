# -*- coding: utf-8 -*-
from rdflib import Graph, RDF, Namespace
import os
import json
import codecs


CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
RDF_UDC_FILE = os.path.join(CONFIG_DIR, 'udcsummary-skos.rdf')
RERO_UDC_FILE = os.path.join(CONFIG_DIR, 'rerodoc_udc.json')
UDC_FILE = os.path.join(CONFIG_DIR, 'udc.json')
UDC = json.load(open(UDC_FILE))


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class UnsupportedError(Error):
    """Exception raised for unknown CUD code.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


def extract_rdf(file_name=RDF_UDC_FILE, lang=["en", "fr", "it", "de"]):

    skos = Namespace("http://www.w3.org/2004/02/skos/core#")
    graph = Graph()
    graph.parse(file_name)
    dictionary = {}
    for concept in graph.subjects(RDF.type, skos.Concept):
        # determine the code
        code = graph.value(concept, skos.notation)
        if not code:
            continue
        # get the preferred language label, there could be more than one
        labels = list(graph.objects(concept, skos.prefLabel))
        labels_in_lang = {}
        if len(labels) > 1:
            for label in labels:
                if label.language in lang:
                    labels_in_lang[label.language] = label.title()
        else:
            label = {labels[0].language: labels[0].title()}
        dictionary[code.title()] = {"uri": concept.title().lower()}
        dictionary[code.title()].update(labels_in_lang)
    return dictionary


def update_udc():
    rero_udc = json.load(open(RERO_UDC_FILE))
    udc_from_rdf = extract_rdf()

    def get_uri(code, udc):
        res = None
        while not res:
            res = udc.get(code)
            if not res:
                code = code[:-1]
            else:
                return udc.get(code, {}).get('uri')
        return None

    for k, v in rero_udc.items():
        #print k, v
        if k.startswith("root"):
            continue
        # range
        if k.find('/') != -1:
            _from, to = k.split('/')
            for code in range(int(_from), int(to) + 1):
                uri = get_uri(str(code), udc_from_rdf)
                #print code, uri
                if uri:
                    v.setdefault('uri', []).append(uri)

        # exact match or parent
        else:
            uri = get_uri(k, udc_from_rdf)
            if uri:
                v['uri'] = [uri]

    json.dump(rero_udc, codecs.open(UDC_FILE, 'w', 'utf-8'), indent=2, ensure_ascii=False)
    UDC = json.load(open(UDC_FILE))
    return True


def get_long_names(lang='en'):

    def concatenate_parent_label(root, values={}, langs=['fr', 'en', 'de', 'it']):
        for ln in langs:
            values.setdefault(ln, []).insert(0, root.get(ln))
        if root.get('parent'):
            concatenate_parent_label(UDC.get(root.get('parent')), values, langs)
        return values
    to_return = {}
    for k, v in UDC.items():
        labels = concatenate_parent_label(v, {})
        if not k.startswith("root_"):
            tmp = {
                "name": u'%s (%s)' % (u' ▸ '.join(labels.get(lang)), k),
                "code": k
            }
            tmp.update(v)
            to_return[k] = tmp
    return to_return


def get_udc(code):
    to_return = UDC.get(code)
    if not to_return:
        raise UnsupportedError(code, 'not used in RERO DOC')
    return to_return
