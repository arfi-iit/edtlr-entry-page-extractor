VENV           = .venv
VENV_BIN       = $(VENV)/bin
VENV_PYTHON    = $(VENV_BIN)/python
VENV_PIP       = $(VENV_BIN)/pip



# Initialize the development environment
init: requirements.txt
	if [ ! -d "$(VENV)" ]; then \
	    python -m venv $(VENV);\
	fi; \
	$(VENV_PIP) install -U pip;
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

# Make the page mappings
mappings: src/extract-page-mappings.py
	$(VENV_PYTHON) src/extract-page-mappings.py;
