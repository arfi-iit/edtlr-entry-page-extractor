#!/usr/bin/env python
"""Extract entry-page mappings from annotated data."""
from argparse import ArgumentParser
from argparse import Namespace


def main():
    """Do the magic."""
    print("OK")


def parse_arguments() -> Namespace:
    """Parse the arguments of the script."""
    parser = ArgumentParser(description='')

    return parser.parse_args()


if __name__ == '__main__':
    main()
