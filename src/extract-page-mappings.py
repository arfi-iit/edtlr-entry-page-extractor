#!/usr/bin/env python
"""Extract entry-page mappings from annotated data."""
from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path
from collections.abc import Generator
from typing import List
from collections import namedtuple
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import re

PAGE_NO_REGEXP = r"(?:\/f)(\d+)\.webp"

Page = namedtuple('Page', ['page_no', 'trascriptions_file'])


def extract_entries(xml_file: Path) -> List[str]:
    """Extract the entries from the specified XML file.

    Parameters
    ----------
    xml_file: Path, required
        The path of the XML file containing the data.

    Returns
    -------
    entries: list of str,
        The list of entries.
    """
    tree = ElementTree.parse(xml_file)
    entries = []
    for element in tree.findall('.//{http://www.w3.org/2001/XInclude}include'):
        entry = element.get('label')
        entries.append(entry)

    return entries


def parse_transcriptions_file(element: Element) -> str | None:
    """Parse the name of the transcriptions file.

    Parameters
    ----------
    element: Element, required
        The XML element from which to parse the transcriptions file path.

    Returns
    -------
    trascriptions_file: str or None
        The path of the transcriptions file.
    """
    value = element.get('corresp')
    return value


def parse_page_no(element: Element) -> int | None:
    """Parse the page number from the provided element.

    Parameters
    ----------
    element: Element, required
        The XML element from which to parse the page number.

    Returns
    -------
    page_no: int or None
        The parsed page number or None.
    """
    img_path = element.get('facs')
    if img_path is None:
        return None

    match = re.search(PAGE_NO_REGEXP, img_path)
    if match is None:
        return None

    value = match.group(1)
    return int(value)


def iter_pages(xml_file: Path) -> Generator[Page, None, None]:
    """Iterate the pages."""
    dir = xml_file.parent
    tree = ElementTree.parse(xml_file)
    for element in tree.findall('.//{http://www.tei-c.org/ns/1.0}pb'):
        page_no = parse_page_no(element)
        transcriptions = parse_transcriptions_file(element)
        if transcriptions is not None:
            yield Page(page_no, dir / transcriptions)
        else:
            yield Page(page_no, None)


def main(root_directory: str, index_file: str):
    """Extract the page data.

    Parameters
    ----------
    root_directory: str, required
        The path of the root data directory.
    index_file: str, required
        The name of the index file within the data directory.
    """
    root_dir = Path(root_directory)
    index_file = root_dir / index_file

    data = []
    for page in iter_pages(index_file):
        if page.trascriptions_file is None:
            continue

        data.extend([(entry, page.page_no)
                     for entry in extract_entries(page.trascriptions_file)])


def parse_arguments() -> Namespace:
    """Parse the arguments of the script."""
    parser = ArgumentParser(
        description='Extract entry-page mappings from annotated data.')
    parser.add_argument('-d',
                        '--directory',
                        help="The root directory of the annotated data.",
                        required=True,
                        type=str)
    parser.add_argument(
        '-i',
        '--index-file',
        help="The name of the index file within root directory.",
        required=False,
        type=str,
        default='index.xml')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.directory, args.index_file)
