"""Run readability measures.

NOTES
-----
This script needs to be run in a py27 environment.
"""

from textstat.textstat import textstatistics

##
##

def fk_grade_group(docs):
    """   """

    ts = textstatistics()

    return [ts.flesch_kincaid_grade(doc.text) for doc in docs]


def smog_group(docs):
    """   """

    ts = textstatistics()

    return [ts.smog_index(doc.text) for doc in docs]


def consensus_group(docs):
    """   """

    ts = textstatistics()

    return [ts.text_standard(doc.text) for doc in docs]


def ar_group(docs):
    """   """

    ts = textstatistics()

    return [ts.automated_readability_index(doc.text) for doc in docs]
