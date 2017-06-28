# -*- coding: utf-8 -*-

import requests

from .constants import HGNC_GENE_FAMILY_URL

HGNC_GENE_FAMILY_OWL_IRI = 'http://ontologies.scai.fraunhofer.de/hgnc_gene_families.owl'


def download(file_path):
    """Downloads HGNC Gene family dump"""
    r = requests.get(HGNC_GENE_FAMILY_URL, stream=True)

    r.raise_for_status()

    with open(file_path, 'w+b') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
