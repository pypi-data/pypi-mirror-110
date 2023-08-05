.PHONY: clean lint format help
.DEFAULT_GOAL := help

PYTHON := python

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
        match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
        if match:
                target, help = match.groups()
                print("\033[36m%-15s\033[0m %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove all build, test, coverage and Python artifacts
	find vmail \
		\( -name '*.py[co]' -o -name '__pycache__' \) -exec rm -rf {} +
	rm -rf build dist .eggs *.egg-info

lint: ## check the Python code syntax and style
	$(PYTHON) -m flake8 vmail

format: ## fix the Python code syntax and imports order
	$(PYTHON) -m isort vmail
	$(PYTHON) -m black vmail

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
