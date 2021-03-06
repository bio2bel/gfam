HGNC Gene Families to BEL
=========================

Further resources can be found: http://www.genenames.org/cgi-bin/genefamilies/

Data is downloaded from: http://www.genenames.org/cgi-bin/genefamilies/download-all/tsv and has the following columns:

- HGNC ID
- Approved Symbol
- Approved Name
- Status
- Previous Symbols
- Synonyms
- Chromosome
- Accession Numbers
- RefSeq IDs
- Gene Family Tag
- Gene family description
- Gene family ID

This file provides an exploded mapping of genes to their gene families. The last 3 are of particular interest for
naming all of the families.

Installation
------------
:code:`pip3 install git+https://github.com/bio2bel/gfam.git`

Running
-------
This script installs a command line tool ``bio2bel_gfam``

1. Deploy to Artifactory with ``bio2bel_gfam arty``
2. Save to folder specified by environment variable ``PYBEL_RESOURCES`` with ``bio2bel_gfam git``

Continuous Integration
----------------------
Resource generation is handled by Travis CI at https://travis-ci.org/bio2bel/gfam (in progress)
