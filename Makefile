# Makefile for Django

# Django-related commands
PYTHON := python
PIP := $(PYTHON) -m pip
MANAGE := $(PYTHON) manage.py

# Targets
install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

app:
	$(MANAGE) startapp $(name)

superuser:
	$(MANAGE) createsuperuser

run:
	$(MANAGE) runserver

test:
	$(MANAGE) test $(name)

shell:
	$(MANAGE) shell

# Additional Django commands
# Add any other commonly used Django commands as needed
# For example:
# - Collect static files: collectstatic
# - Run a specific management command: mycommand
# - And more...

help:
	@echo "Django Makefile Help"
	@echo "----------------------"
	@echo "Available targets:"
	@echo "  install         - Install application dependencies"
	@echo "  install-dev     - Install development dependencies"
	@echo "  clean           - Remove Python artifacts"
	@echo "  makemigrations  - Create database migrations"
	@echo "  migrate         - Apply database migrations"
	@echo "  app name=       - Create a new Django app"
	@echo "  superuser       - Create a superuser"
	@echo "  run             - Run the Django development server"
	@echo "  test name=      - Run tests for a specific app"
	@echo "  shell           - Run a Django shell"
	@echo "  help            - Display this help message"

.PHONY: install install-dev clean makemigrations migrate app superuser run test shell help
