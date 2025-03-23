#!/usr/bin/env python
"""Extract entry-page mappings from annotated data."""
from argparse import ArgumentParser
from argparse import Namespace
from itertools import takewhile
from pandas import DataFrame
from pathlib import Path
from rcf import normalize
from typing import List
from xml.etree import ElementTree
import csv
import logging
import re


class XPath:
    """XPath selectors for input files."""

    TitleWord = ".//div[@class='headword]"
    Buttons = ".//{http://www.w3.org/1999/xhtml}button"


class Mapping:
    """Represents the mapping of an entry title word to the collection of pages."""

    def __init__(self, title_word: str, pages: List[int]):
        """Initialize the current instance.

        Parameters
        ----------
        title_word: str, required
            The title word of the entry.
        pages: list of int, required
            The list of entry pages.
        """
        self.__title_word = title_word
        self.__pages = sorted(pages)
        self.__stem = self.__extract_stem(title_word)

    @property
    def title_word(self):
        """Get the title word."""
        return self.__title_word

    @property
    def stem(self):
        """Get the stem of the title word."""
        return self.__stem

    @property
    def pages(self):
        """Get the pages of the entry."""
        return self.__pages

    def __extract_stem(self, title_word: str) -> str:
        """Extract the stem from the provided title word.

        Parameters
        ----------
        title_word: str, required
            The title word.

        Returns
        -------
        stem: str
            The stem (first complete word in capitals) of the title word.
        """

        def is_upper_letter(chr: str) -> bool:
            return chr.isupper() and chr.isalpha()

        stem = "".join([c for c in takewhile(is_upper_letter, title_word)])
        return normalize(stem)


def extract_mapping(input_file: Path) -> Mapping | None:
    """Extract the mapping from the input file.

    Parameters
    ----------
    input_file: Path, required
        The path of the input file.

    Returns
    -------
    mapping: Mapping
        The mapping extracted from the file or None.
    """
    tree = ElementTree.parse(input_file)
    if tree.getroot().tag != '{http://www.w3.org/1999/xhtml}article':
        return []

    title_word = None
    for elem in tree.iter('{http://www.w3.org/1999/xhtml}div'):
        if elem.get("class") == "headword":
            title_word = elem.text
            break

    if title_word is None:
        return None

    pages = []
    for btn in tree.iter('{http://www.w3.org/1999/xhtml}button'):
        match = re.search(r'\d+', btn.text)
        if match is None:
            continue

        try:
            page_no = int(match.group())
            pages.append(page_no)
        except ValueError:
            continue

    return Mapping(title_word, pages)


def save_to_csv(mappings: List[Mapping], file_name: str):
    """Save the mappings to the output file in the CSV format.

    Parameters
    ----------
    data: list of Mapping instances, required
        The data to save.
    file_name: str, required
        The name of the file in which to save data.
    """
    data = []
    for m in mappings:
        pages = ",".join([str(p) for p in m.pages])
        first_page, last_page = m.pages[0], m.pages[-1]
        data.append((m.stem, m.title_word, pages, first_page, last_page))
    df = DataFrame(
        data, columns=['stem', 'entry', 'page_no', 'first_page', 'last_page'])
    df = df.sort_values(by=['stem', 'first_page'])

    df.to_csv(file_name,
              index=False,
              header=False,
              columns=['entry', 'page_no'],
              quoting=csv.QUOTE_ALL)


def main(root_directory: str, output_file: str = 'mappings.csv'):
    """Extract the page data.

    Parameters
    ----------
    root_directory: str, required
        The path of the root data directory.
    output_file: str, optional
        The name of the output file.
    """
    root_dir = Path(root_directory)
    mappings = []
    for file in root_dir.rglob('*'):
        if file.is_dir():
            continue

        try:
            logging.info(f"Extracting mappings from {file}.")
            mapping = extract_mapping(file)
            mappings.append(mapping)

        except Exception as ex:
            logging.error(f"Erorr extracting mapping from {file}.",
                          exc_info=ex)

    save_to_csv(mappings, output_file)


def parse_arguments() -> Namespace:
    """Parse the arguments of the script."""
    parser = ArgumentParser(
        description='Extract entry-page mappings from annotated data.')
    parser.add_argument('-d',
                        '--directory',
                        help="The root directory of the annotated data.",
                        required=True,
                        type=str)

    parser.add_argument('-o',
                        '--output-file',
                        help="The path of the output CSV file.",
                        required=False,
                        type=str,
                        default='mappings.csv')
    parser.add_argument(
        '--log-level',
        help="The level of details to print when running.",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=getattr(logging, args.log_level))
    main(args.directory, args.output_file)

    logging.info("That's all folks!")
