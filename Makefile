VENV           = .venv
VENV_BIN       = $(VENV)/bin
VENV_PYTHON    = $(VENV_BIN)/python
VENV_PIP       = $(VENV_BIN)/pip

# Cleanup
clean:
	rm -rf "$(VENV)" *.csv;

venv: clean
	python -m venv $(VENV);
	$(VENV_PIP) install -U pip;

# Initialize the development environment
dev-init: venv
	if [ -f requirements-dev.txt ]; then \
	    $(VENV_PIP) install -r requirements-dev.txt;\
	else \
	    $(VENV_PIP) install python-lsp-server[all] \
		yapf \
		cmake-language-server \
		autotools-language-server; \
	    $(VENV_PIP) freeze > requirements-dev.txt; \
	fi;\
	$(VENV_PIP) install -r requirements.txt;

init: venv
	$(VENV_PIP) install -r requirements.txt;

# Make the page mappings
# Example invocations:
#     make mappings DATA_DIR=<path to data directory>
#     make mappings \
#         DATA_DIR=<path to data directory> \
#         INDEX_FILE=<name of the index XML file>;
INDEX_FILE=index.xml
OUTPUT_FILE=mappings.csv
mappings: src/extract-page-mappings.py
	test -n "$(DATA_DIR)";
	$(VENV_PYTHON) src/extract-page-mappings.py \
		-d $(DATA_DIR) \
		-i $(INDEX_FILE) \
		-o $(OUTPUT_FILE);

.PHONY: clean
