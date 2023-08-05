# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Specker JSON Specification Validator,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
.PHONY: $(shell egrep "^([a-zA-Z\_\-]+):" Makefile | cut -d: -f 1)
.EXPORT_ALL_VARIABLES:
.DEFAULT_TARGET: help

HAVE_PYTHON := $(shell which python3)
ifeq ($(HAVE_PYTHON), )
	$(error "Unable to locate python3")
endif
HAVE_PIP := $(shell python3 -c 'help("modules")' | grep " pip ")
ifeq ($(HAVE_PIP), )
	$(error "Unable to locate python pip")
endif

PYTHON_VERSION := $(shell $(HAVE_PYTHON) --version | awk '{print $$2;}' | sed -r 's/\.[0-9]{1,}$$//g')

PROJECT_NAME := $(shell egrep "^name =" pyproject.toml | awk '{print $$3}' | tr -d '"')
PROJECT_VERSION := $(shell egrep "^version =" pyproject.toml | awk '{print $$3}' | tr -d '"')

THIS_DIR := $(shell pwd)

help:
	@egrep "^[a-zA-Z_-]+:.*?## .*$$" Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

docs:  ## Generate Documentation
	doxygen

lint:  ## Linting
	python3 -m pylint --rcfile .pylintrc --recursive true --output-format parseable src/ 
	python3 -m mypy --config-file .mypy.ini src/

build: update_python_version  ## Build Python Package
	python3 -m build
	python3 -m twine check --strict dist/*

update_python_version:  ## Update Minimum Python Version, based on version of current systems python version
	sed -ri "s/^requires-python .*/requires-python = \">=${PYTHON_VERSION}\"/g" pyproject.toml

update_project_version:  ## Update Project Version to version specified by NEW_VERSION= at runtime
	test -n "${NEW_VERSION}" || exit 1
	sed -ri "s/^version .*/version = \"${NEW_VERSION}\"/g" pyproject.toml
	sed -ri "s/^PROJECT_NUMBER.*/PROJECT_NUMBER = \"${NEW_VERSION}\"/g" Doxyfile

install:  ## Install
	@echo "Installing ${PROJECT_NAME}@${PROJECT_VERSION}"
	python3 -m pip install file://$$(pwd)/dist/${PROJECT_NAME}-${PROJECT_VERSION}.tar.gz --force-reinstall

dist:  ## Distribute to PyPi
	TWINE_USERNAME="__token__" TWINE_PASSWORD="${DIST_PASSWORD}" python3 -m twine upload --non-interactive -c "${PROJECT_NAME}, Version: ${PROJECT_VERSION}" dist/*

tag:  ## Create Git Tags
	JOB_TOKEN="${DIST_PASSWORD}" ./git-tags.sh

clean:  ## Clean up
	rm -rf docs/
	rm -rf dist/
	rm -rf src/*.egg-info
	rm -rf .mypy_cache

install_build_deps:  ## Install Build Dependencies
	python3 -m pip install -r build_requirements.txt
