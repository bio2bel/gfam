# -*- coding: utf-8 -*-

from __future__ import print_function

import click

from . import to_bel as to_bel_pkg


@click.group()
def main():
    """Output gene family hierarchy as BEL script and BEL namespace"""
    to_bel_pkg.add_to_pybel_resources()


if __name__ == '__main__':
    main()
