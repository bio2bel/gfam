# -*- coding: utf-8 -*-

"""Run this script with either :code:`python3 -m bio2bel_gfam arty` or :code:`python3 -m bio2bel_gfam git`"""

from __future__ import print_function

import logging

import click

from .to_bel import add_to_pybel_resources, deploy_to_arty


@click.group()
def main():
    """Output gene family hierarchy as BEL script and BEL namespace"""
    logging.basicConfig(level=10, format="%(asctime)s - %(levelname)s - %(message)s")


@main.command()
def git():
    """Save to git repository"""
    add_to_pybel_resources()


@main.command()
def arty():
    """Deploy to artifactory"""
    deploy_to_arty()


if __name__ == '__main__':
    main()
