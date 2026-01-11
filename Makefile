# Force bash for Makefile recipes (needed for features like 'source'); 
# without it, Make would use /bin/sh and these commands could fail.
SHELL := /bin/bash
# Resolve absolute path to the directory containing this Makefile; 
# without it, ROOT_DIR references (e.g., in format target) would break when running from other locations.
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# INSTALL DEPENDENCIES
activate:
	source .venv/bin/activate ;

install-dev:
	uv init ; \
	python3 -m venv .venv ; \
	source .venv/bin/activate ; \
	uv add -r requirements-dev.txt

# FORMAT CODE
format:
	cd ${ROOT_DIR}/src; isort .; black .;
	cd ${ROOT_DIR}/tests; isort .; black .;

# RUN THE APPLICATION LOCALLY
run:
	source .venv/bin/activate ; \
	uvicorn main:app --port 8080 --reload

# TEST
test-unit:
	pytest --verbose --color=yes tests/unit

test-coverage:
	coverage run -m pytest --verbose --color=yes tests/unit
	coverage report -m
