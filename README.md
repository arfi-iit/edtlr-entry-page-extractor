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
