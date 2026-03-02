# ------------------------
# Help
# ------------------------
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make setup            - Install project, dev, and test dependencies"
	@echo "  make install-project  - Install main/runtime dependencies"
	@echo "  make install-dev      - Install dev dependencies (e.g., pyrefly, lefthook)"
	@echo "  make install-test     - Install test dependencies (e.g., pytest)"
	@echo "  make lint             - Run Ruff + Pyrefly checks"
	@echo "  make test             - Run pytest tests"

# ------------------------
# Dependency installation
# ------------------------
.PHONY: setup
setup: install-project install-dev install-test install-pre-commit
	@echo "✅ Project setup complete!"

.PHONY: install-project
install-project:
	@echo "📚️ Installing project dependencies..."
	@uv sync --no-group dev --no-group test

.PHONY: install-dev
install-dev:
	@echo "🔧 Installing dev dependencies..."
	@uv sync --group dev

.PHONY: install-test
install-test:
	@echo "🧪 Installing test dependencies..."
	@uv sync --group test

# ------------------------
# Pre-commit hooks
# ------------------------
.PHONY: install-pre-commit
install-pre-commit:
	@echo "🔧 Installing pre-commit hooks..."
	@uv run lefthook install

# ------------------------
# Linting
# ------------------------
.PHONY: lint
lint:
	@echo "🔧 Running Ruff lint..."
	@uv run ruff check --fix .
	@echo "🔧 Running Ruff format..."
	@uv run ruff format .
	@echo "🔧 Running Pyrefly type-checks..."
	@uv run pyrefly check

# ------------------------
# Tests
# ------------------------
.PHONY: test
test:
	@echo "🧪 Running tests..."
	@uv run pytest