SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
# $(MAKEFILE_LIST)
# Special built in variable in make. Is contains the list of all Makefile names that haven been parsed up to this point. The first item in this list is typically the path to the current Makefile

# $(firstword $(MAKEFILE_LIST))
# Extracts the first item from the list of Makefile names

# $(realpath $(firstword $(MAKEFILE_LIST)))
# Resolves the absolute path of the Makefile, converting any relative paths to absolute paths

# $(shell dirname $(realpath $(firstowrd $(MAKEFILE_LIST))))
# Runs a shell command and caputes its output
# dirname is a Unix command that extracts the directory portion of a file path.

install:
	pip install -r requirements.txt

format:
	cd ${ROOT_DIR}/API; isort .; black .;
	cd ${ROOT_DIR}/tests; isort .; black .;

run:
	python API/main.py

test-unit:
	pytest --verbose --color=yes tests/unit_tests

test-coverage:
	coverage run -m pytest --verbose --color=yes tests/unit
	coverage report -m