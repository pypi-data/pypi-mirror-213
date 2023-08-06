.DEFAULT_GOAL := help

.PHONY: docs test type-check fmt ci

test: ## Run tests
	pytest

type-check: ## Check all python types
	mypy geopic_tag_reader/

fmt: ## Format code
	black --fast .

ci: type-check fmt test ## Run all check like the ci

docs:  ## Generates documentation from Typer embedded docs
	python -m typer_cli ./geopic_tag_reader/main.py utils docs --name geopic-tag-reader --output docs/CLI_USAGE.md
	lazydocs --overview-file API_USAGE.md --ignored-modules main --output-path docs/ geopic_tag_reader/

help: ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
