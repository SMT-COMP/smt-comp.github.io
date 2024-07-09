.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@poetry shell

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking for obsolete submissions/Readme.md"
	@poetry run python3 submissions/template/generate_Readme.py check
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry . --extend-exclude "archive|_site"

.PHONY: test generation
test: generation ## Test the code with pytest
	@echo "🚀 Generating submissions/Readme.md"
	@poetry run python3 submissions/template/generate_Readme.py generate
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest

generation: submission-generation participant-data ## Files generation for the website

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

GENERATED_SCHEMA_FILE=web/content/solver_submission/schema.json
GENERATED_SCHEMA_HTML=web/content/solver_submission/schema.html
PARTICIPANT_DATA_FILE=web/data/participants.json

.PHONY: submission-doc submission-generation participant-data
submission-generation:
	@echo "🚀 Generating schema to $(GENERATED_SCHEMA_FILE)"
	@poetry run smtcomp dump-json-schema $(GENERATED_SCHEMA_FILE)

submission-doc: submission-generation
	@echo "🚀 Generating html doc to $(GENERATED_SCHEMA_HTML)"
	@echo "    Needs 'pip install json-schema-for-humans'"
	@poetry run generate-schema-doc --expand-buttons --no-link-to-reused-ref $(GENERATED_SCHEMA_FILE) $(GENERATED_SCHEMA_HTML)

participant-data:
	@echo "🚀 Generating participant data to $(PARTICIPANT_DATA_FILE)"
	@poetry run smtcomp show-json submissions/*.json $(PARTICIPANT_DATA_FILE)

hugo-server:
	(cd web; hugo server)
