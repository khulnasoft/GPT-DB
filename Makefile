.DEFAULT_GOAL := help

SHELL=/bin/bash
VENV = venv
CONDA_ENV = gptdb_env

# Detect the operating system and set the virtualenv bin directory
ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

.PHONY: conda-install
conda-install: ## Download and install Conda if not installed
	@if ! command -v conda &> /dev/null; then \
		echo "Conda is not installed on your system."; \
		echo "Downloading and installing Miniconda..."; \
		OS=$(shell uname -s); \
		if [ "$$OS" = "Linux" ]; then \
			URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"; \
		elif [ "$$OS" = "Darwin" ]; then \
			URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"; \
		else \
			echo "Unsupported operating system: $$OS"; \
			exit 1; \
		fi; \
		echo "Downloading Miniconda from: $$URL"; \
		curl -o miniconda-installer.sh $$URL; \
		echo "Installing Miniconda..."; \
		bash miniconda-installer.sh -b -p $$HOME/miniconda; \
		rm miniconda-installer.sh; \
		echo "Adding Conda to PATH..."; \
		export PATH=$$HOME/miniconda/bin:$$PATH; \
		echo "Miniconda installation completed."; \
	else \
		echo "Conda is already installed. Version:"; \
		conda --version; \
	fi

.PHONY: conda-activate
conda-activate: ## Activate the specified Conda environment
	@if ! command -v conda &> /dev/null; then \
		echo "Conda is not installed. Run 'make conda-install' first."; \
		exit 1; \
	fi; \
	ENV_NAME=gptdb_env; \
	if ! conda info --envs | grep -q "$$ENV_NAME"; then \
		echo "Environment '$$ENV_NAME' does not exist. Creating it..."; \
		conda create -n $$ENV_NAME python=3.10 -y; \
	fi; \
	echo "Activating the Conda environment '$$ENV_NAME'..."; \
	$$HOME/miniconda/bin/conda activate $$ENV_NAME || echo "Run the following command to activate the environment manually in your shell:"; \
	echo "source $$HOME/miniconda/bin/activate $$ENV_NAME"



# Virtual environment setup
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
	# Install dependencies for testing
	$(VENV_BIN)/pip install -e ".[openai]"
	touch $(VENV)/.testenv

.PHONY: fmt
fmt: setup ## Format Python code
	$(VENV_BIN)/isort gptdb/
	$(VENV_BIN)/isort --extend-skip="examples/notebook" examples
	$(VENV_BIN)/black --extend-exclude="examples/notebook" .
	$(VENV_BIN)/blackdoc gptdb
	$(VENV_BIN)/blackdoc examples
	$(VENV_BIN)/flake8 gptdb/core/ gptdb/rag/ gptdb/storage/ gptdb/datasource/ gptdb/client/ gptdb/agent/ gptdb/vis/ gptdb/experimental/

.PHONY: fmt-check
fmt-check: setup ## Check Python code formatting and style without making changes
	$(VENV_BIN)/isort --check-only gptdb/
	$(VENV_BIN)/isort --check-only --extend-skip="examples/notebook" examples
	$(VENV_BIN)/black --check --extend-exclude="examples/notebook" .
	$(VENV_BIN)/blackdoc --check gptdb examples
	$(VENV_BIN)/flake8 gptdb/core/ gptdb/rag/ gptdb/storage/ gptdb/datasource/ gptdb/client/ gptdb/agent/ gptdb/vis/ gptdb/experimental/

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
	conda deactivate || true
	conda remove --name $(CONDA_ENV) --all -y || true
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
help: ## Display this help screen
	@echo "Available commands:"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort
