flake8:
	../venv/bin/flake8 .

mypy:
	../venv/bin/mypy .

test:
	../venv/bin/pytest -s $(PYTEST_ME_PLEASE)

check: test flake8 mypy
