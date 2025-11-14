.PHONY: help install test format lint clean run

help:
	@echo "LLMCode - AI Coding Assistant"
	@echo ""
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make test      - Run tests"
	@echo "  make format    - Format code with black"
	@echo "  make lint      - Lint code with ruff"
	@echo "  make clean     - Clean build artifacts"
	@echo "  make run       - Run interactive mode"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

format:
	black llmcode/ tests/ examples/

lint:
	ruff check llmcode/ tests/ examples/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	llmcode

setup:
	bash setup.sh
