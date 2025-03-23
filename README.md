# eDTLR entry-page extractor

This utility extracts the mappings between dictionary entries and their pages from the data that powers the site [https://clre.solirom.ro](https://clre.solirom.ro/).

## Usage

To use this utility, you must have the data available on your computer.

### Clone this repository

To clone the repository run the following command in you terminal:

```shell
git clone https://github.com/arfi-iit/edtlr-entry-page-extractor.git
```

### Install dependencies

To install the dependencies required for running this utility, navigate to the directory containing this repository, and run in the terminal:

```shell
make init
```

### Extract mappings

To extract the mappings, navigate to the directory containing this repository, and run the following command in terminal. Don't forget to replace `<data directory>` with the path to the actual directory that contains the data.

```shell
make mappings DATA_DIR=<data directory>
```

The command above will create a file called `mappings.csv` which contains the mappings between the entries and their pages.

### Split mappings (optional)

If the data directory contains entries for multiple dictionary volumes, then the `mappings.csv` file needs to be split manually. For example, the `mappings.csv` file extracted for the entries starting with the letter `L` are split into two dictionary volumes.

As such, the `mappings.csv` file contains the following data:
```
"LHERZOLÍT s. n."     "778"
"LHERZOLÍTĂ s. f."    "778"
"LI interj."          "1"
"LIA interj."         "1"
```

The data above denotes that the first volume ends at page 778 with the entry `LHERZOLÍTĂ`, and the second volume starts wit the entry `LI`. In such case, **the user must split the file into multiple ones**.
