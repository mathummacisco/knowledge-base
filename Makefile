# =============================================================================
# Knowledge Base — root Makefile
#
# This is the supported entrypoint for everyday contributor workflows. Targets
# match what CI runs, so a green `make check` is equivalent to a green CI run.
#
# Quickstart:
#   make setup     # one-time: create .venv and install deps
#   make serve     # live preview at http://127.0.0.1:8000
#   make check     # run all validators (same as CI gate)
#   make ship MSG="..."  # check + commit + push
#   make help      # list all targets
# =============================================================================

# Use a project-local .venv to match what onboarding.md tells new contributors.
# If the repo .venv exists, use it; otherwise fall back to the user's python3
# (and remind them to run `make setup`).
VENV       := .venv
VENV_BIN   := $(VENV)/bin
PY         := $(shell test -x $(VENV_BIN)/python && echo $(VENV_BIN)/python || echo python3)
MKDOCS     := $(shell test -x $(VENV_BIN)/mkdocs && echo $(VENV_BIN)/mkdocs || echo mkdocs)

# Knobs that suppress chatty plugin output without changing behavior.
MKDOCS_ENV := DISABLE_MKDOCS_2_WARNING=true GIT_COMMITTERS_ENABLED=false

# Default port for the dev server. Override with `make serve PORT=8080`.
PORT       := 8000

# Phony so make never confuses a target with a file of the same name.
.PHONY: help setup serve build check ci-check \
        frontmatter links images stale \
        landings clean ship status \
        $(MAKECMDGOALS)

.DEFAULT_GOAL := help

# -----------------------------------------------------------------------------
# Help — generated from `## comment` markers above each target.
# -----------------------------------------------------------------------------
help: ## Show this help.
	@echo ""
	@echo "Knowledge Base — make targets"
	@echo "=============================="
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*## / { printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "Tips:"
	@echo "  - First time?       run 'make setup'"
	@echo "  - Writing docs?     run 'make serve' in one terminal, edit in the other"
	@echo "  - Pre-push gate?    run 'make check' (validators + strict build + stale)"
	@echo "  - CI gate locally?  run 'make ci-check' (what GitHub Actions runs)"
	@echo "  - Custom port?      'make serve PORT=8080'"
	@echo ""

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
setup: ## One-time: create .venv and install docs deps.
	@if [ ! -d $(VENV) ]; then \
		echo ">> Creating $(VENV)…"; \
		python3 -m venv $(VENV); \
	fi
	@echo ">> Installing requirements-docs.txt into $(VENV)…"
	@$(VENV_BIN)/pip install --quiet --upgrade pip
	@$(VENV_BIN)/pip install --quiet -r requirements-docs.txt
	@echo ">> Done. Run 'make serve' to start the dev server."

# -----------------------------------------------------------------------------
# Local preview + build
# -----------------------------------------------------------------------------
serve: ## Live preview with hot-reload (default port 8000; override with PORT=).
	@echo ">> Serving on http://127.0.0.1:$(PORT)"
	@$(MKDOCS_ENV) $(MKDOCS) serve -a 127.0.0.1:$(PORT)

build: ## Strict build into ./site (matches CI build step).
	@echo ">> Building site (strict)…"
	@$(MKDOCS_ENV) $(MKDOCS) build --strict

# -----------------------------------------------------------------------------
# Validation — these match CI exactly.
# -----------------------------------------------------------------------------
check: frontmatter links images stale build ## Pre-push gate. All validators incl. stale + strict build.
	@echo ""
	@echo "✅ All checks passed. Safe to push."

ci-check: frontmatter links images build ## CI gate. Excludes stale (so per-doc staleness doesn't fail unrelated PRs).
	@echo ""
	@echo "✅ CI checks passed."

frontmatter: ## Validate YAML frontmatter on every doc.
	@$(PY) scripts/check-frontmatter.py

links: ## Resolve every internal link and anchor.
	@$(PY) scripts/check-links.py

images: ## Enforce the 200 KB per-image budget.
	@$(PY) scripts/check-image-budget.py

stale: ## Report docs past their review_cadence window.
	@$(PY) scripts/stale-report.py

# -----------------------------------------------------------------------------
# Maintenance
# -----------------------------------------------------------------------------
landings: ## Regenerate auto-generated section card-grid landings (idempotent).
	@$(PY) scripts/regen-section-landings.py

status: ## Show git status + recent commits + last 3 workflow runs.
	@git status --short
	@echo ""
	@echo "Recent commits:"
	@git log --oneline -5
	@echo ""
	@echo "Last 3 workflow runs:"
	@gh run list --branch main --limit 3 2>/dev/null || echo "  (gh CLI not authenticated)"

clean: ## Remove site/, __pycache__, and .pytest_cache.
	@rm -rf site/ scripts/__pycache__/ .pytest_cache/
	@echo ">> Cleaned site/, __pycache__/, .pytest_cache/"

# -----------------------------------------------------------------------------
# Ship — gated commit + push. Requires MSG="…".
# -----------------------------------------------------------------------------
ship: ## Run checks, commit -A, and push. Requires MSG="commit message".
	@if [ -z "$(MSG)" ]; then \
		echo "❌ MSG is required."; \
		echo "   Usage: make ship MSG=\"docs(scope): what changed\""; \
		exit 1; \
	fi
	@echo ">> Running checks before ship…"
	@$(MAKE) --no-print-directory check
	@echo ""
	@echo ">> Staging all changes…"
	@git add -A
	@if git diff --cached --quiet; then \
		echo "❌ Nothing staged. Aborting."; \
		exit 1; \
	fi
	@echo ">> Committing…"
	@git commit -m "$(MSG)"
	@echo ">> Pushing to origin…"
	@git push
	@echo ""
	@echo "✅ Shipped. Check workflow runs with 'make status'."
