.PHONY: freeze
freeze:
	pip freeze>requirements.txt

.PHONY:tests
tests:
	# run those tests
	pytest . --doctest-modules

.PHONY: black
black:
	black

.PHONY: flake8
flake8:
	flake8

.PHONY: package
package:
	poetry build

.PHONY: coverage
coverage:
	coverage run --source=copyright_shared_lambda -m pytest . && coverage report && coverage html

.PHONY: build
build: black flake8 coverage
build:
	echo "formatting, linting, testing and packaging"

.PHONY: .build
.build: build
	echo "Running default target: build"