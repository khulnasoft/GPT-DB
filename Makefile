.DEFAULT_GOAL := help

SHELL=/bin/bash
VENV = venv

# Detect the operating system and set the virtualenv bin directory
ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

setup: $(VENV)/bin/activate

$(VENV)/bin/activate: $(VENV)/.venv-timestamp

$(VENV)/.venv-timestamp: setup.py requirements
	# Create new virtual environment if setup.py has changed
	python3 -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements/dev-requirements.txt
	$(VENV_BIN)/pip install -r requirements/lint-requirements.txt
	touch $(VENV)/.venv-timestamp

testenv: $(VENV)/.testenv

$(VENV)/.testenv: $(VENV)/bin/activate
	# $(VENV_BIN)/pip install -e ".[framework]"
	$(VENV_BIN)/pip install -e ".[openai]"
	touch $(VENV)/.testenv


.PHONY: fmt
fmt: setup ## Format Python code
	$(VENV_BIN)/isort gptdb/
	$(VENV_BIN)/isort --extend-skip="examples/notebook" examples
	$(VENV_BIN)/black --extend-exclude="examples/notebook" .
	$(VENV_BIN)/blackdoc gptdb
	$(VENV_BIN)/blackdoc examples

.PHONY: fix
fix: setup ## Automatically fix linting and formatting errors
	$(VENV_BIN)/isort gptdb/ --apply
	$(VENV_BIN)/isort --extend-skip="examples/notebook" examples --apply
	$(VENV_BIN)/black --extend-exclude="examples/notebook" .
	$(VENV_BIN)/blackdoc gptdb
	$(VENV_BIN)/blackdoc examples
	$(VENV_BIN)/flake8 gptdb/core/ gptdb/rag/ gptdb/storage/ gptdb/datasource/ gptdb/client/ gptdb/agent/ gptdb/vis/ gptdb/experimental/ --ignore=E501 --quiet

.PHONY: fmt-check
fmt-check: setup ## Check Python code formatting and style without making changes
	$(VENV_BIN)/isort --check-only gptdb/
	$(VENV_BIN)/isort --check-only --extend-skip="examples/notebook" examples
	$(VENV_BIN)/black --check --extend-exclude="examples/notebook" .
	$(VENV_BIN)/blackdoc --check gptdb examples
	$(VENV_BIN)/flake8 gptdb/core/ gptdb/rag/ gptdb/storage/ gptdb/datasource/ gptdb/client/ gptdb/agent/ gptdb/vis/ gptdb/experimental/ --ignore=E501 --quiet

.PHONY: pre-commit
pre-commit: fmt-check test test-doc mypy ## Run formatting and unit tests before committing

test: $(VENV)/.testenv ## Run unit tests
	$(VENV_BIN)/pytest gptdb

.PHONY: test-doc
test-doc: $(VENV)/.testenv ## Run doctests
	$(VENV_BIN)/pytest --doctest-modules -k "not test_" gptdb/core

.PHONY: mypy
mypy: $(VENV)/.testenv ## Run mypy checks
	$(VENV_BIN)/mypy --config-file .mypy.ini gptdb/rag/ gptdb/datasource/ gptdb/client/ gptdb/agent/ gptdb/vis/ gptdb/experimental/

.PHONY: coverage
coverage: setup ## Run tests and report coverage
	$(VENV_BIN)/pytest gptdb --cov=gptdb

.PHONY: clean
clean: ## Clean up the environment
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.coverage' -delete

.PHONY: clean-dist
clean-dist: ## Clean up the distribution
	rm -rf dist/ *.egg-info build/

.PHONY: package
package: clean-dist ## Package the project for distribution
	IS_DEV_MODE=false python setup.py sdist bdist_wheel

.PHONY: upload
upload: ## Upload the package to PyPI
	twine upload dist/*

.PHONY: help
help:  ## Display this help screen
	@echo "Available commands:"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort
