# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import os

import pandas as pd
from pybel.constants import IS_A
from pybel.utils import ensure_quotes
from pybel_tools.constants import PYBEL_RESOURCES_ENV
from pybel_tools.definition_utils import write_namespace, get_date
from pybel_tools.document_utils import write_boilerplate
from pybel_tools.resources import HGNC_HUMAN_GENES, HGNC_GENE_FAMILIES, CONFIDENCE
from pybel_tools.resources import deploy_namespace, deploy_knowledge

from .constants import HGNC_GENE_FAMILY_URL

log = logging.getLogger(__name__)

HGNC_GENE_FAMILIES_NAMESPACE_MODULE_NAME = 'hgnc-gene-families'
HGNC_GENE_FAMILIES_MEMBERSHIP_MODULE_NAME = 'hgnc-gene-family-membership'


def get_data():
    """Gets the source data.
    
    :return: A data frame containing the original source data
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(HGNC_GENE_FAMILY_URL, sep='\t')
    return df


def get_gfam_names(df=None):
    """Processes the source data.
    
    :param pandas.DataFrame df: A data frame containing the original data source
    :return: Returns the set of current HGNC Gene Family names
    :rtype: set[str]
    """
    df = get_data() if df is None else df
    entries = set(df['Gene family description'].unique())
    return entries


def write_belns(file, df=None):
    """Writes the HGNC Gene Families as a BEL namespace file.
    
    :param file file: A writable file or file-like 
    :param pandas.DataFrame df: A data frame containing the original data source
    """
    values = get_gfam_names(df=df)

    write_namespace(
        namespace_name="HGNC Gene Families",
        namespace_keyword="GFAM",
        namespace_domain="Gene and Gene Products",
        namespace_species='9606',
        namespace_description="HUGO Gene Nomenclature Committee (HGNC) curated gene families",
        citation_name=HGNC_GENE_FAMILY_URL,
        author_name='Charles Tapley Hoyt',
        author_contact="charles.hoyt@scai.fraunhofer.de",
        author_copyright='Creative Commons by 4.0',
        values=values,
        functions="GRP",
        file=file
    )


def write_hgnc_gene_families(file, df=None):
    """Writes the HGNC gene family hierarchy a BEL script.
    
    :param file file: A writable file or file-like
    :param pandas.DataFrame df: A data frame containing the original data source
    """
    df = get_data() if df is None else df

    write_boilerplate(
        document_name='HGNC Gene Family Definitions',
        authors='Charles Tapley Hoyt',
        contact='charles.hoyt@scai.fraunhofer.de',
        licenses='Creative Commons by 4.0',
        copyright='Copyright (c) 2017 Charles Tapley Hoyt. All Rights Reserved.',
        description="""This BEL document represents the gene families curated by HGNC, describing various functional, structural, and logical classifications""",
        namespace_dict={
            'HGNC': HGNC_HUMAN_GENES,
            'GFAM': HGNC_GENE_FAMILIES,
        },
        namespace_patterns={},
        annotations_dict={'Confidence': CONFIDENCE},
        annotations_patterns={},
        file=file
    )

    print('SET Citation = {"PubMed","HGNC","25361968"}', file=file)
    print('SET Evidence = "HGNC Definitions"', file=file)
    print('SET Confidence = "Axiomatic"', file=file)

    for _, gfam, gene in df[['Gene family description', 'Approved Symbol']].itertuples():
        gfam_clean = ensure_quotes(gfam.strip())
        gene_clean = ensure_quotes(gene.strip())

        print('g(HGNC:{}) {} g(GFAM:{})'.format(gene_clean, IS_A, gfam_clean), file=file)


def add_to_pybel_resources():
    """Gets the data and writes BEL namespace files to the PyBEL resources directory"""
    if PYBEL_RESOURCES_ENV not in os.environ:
        raise ValueError('{} not in os.environ'.format(PYBEL_RESOURCES_ENV))

    log.info('pybel resources at: %s', os.environ[PYBEL_RESOURCES_ENV])

    df = get_data()

    namespace_path = os.path.join(os.environ[PYBEL_RESOURCES_ENV], 'namespace', HGNC_GENE_FAMILIES_NAMESPACE_MODULE_NAME + '.belns')
    with open(namespace_path, 'w') as file:
        write_belns(file, df=df)

    membership_path = os.path.join(os.environ[PYBEL_RESOURCES_ENV], 'knowledge', HGNC_GENE_FAMILIES_MEMBERSHIP_MODULE_NAME + '.bel')
    with open(membership_path, 'w') as file:
        write_hgnc_gene_families(file, df=df)


def deploy_to_arty():
    """Gets the data and writes BEL namespace file to artifactory"""
    df = get_data()

    # Deploy Namespace

    arty_qname = '{}-{}.belns'.format(HGNC_GENE_FAMILIES_NAMESPACE_MODULE_NAME, get_date())

    with open(arty_qname, 'w') as file:
        write_belns(file, df=df)

    deploy_namespace(arty_qname, HGNC_GENE_FAMILIES_NAMESPACE_MODULE_NAME)

    # Deploy Membership Knowledge

    arty_qname = '{}-{}.bel'.format(HGNC_GENE_FAMILIES_MEMBERSHIP_MODULE_NAME, get_date())

    with open(arty_qname, 'w') as file:
        write_hgnc_gene_families(file, df=df)

    deploy_knowledge(arty_qname, HGNC_GENE_FAMILIES_MEMBERSHIP_MODULE_NAME)
