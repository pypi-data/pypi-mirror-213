include Make.defs

.PHONY: venv
venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && pip install -Ur requirements.txt
	touch venv/touchfile

.PHONY: help
help: Makefile  # Print this message
	$(call usage)

.PHONY: ruff
ruff:  # Ruff linter
	$(ACTIVATE) ruff check .

.PHONY: fix
fix:  # Auto fix lint violations
	$(ACTIVATE) ruff check . --fix
