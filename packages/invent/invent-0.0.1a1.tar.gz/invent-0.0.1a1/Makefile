SHELL := /bin/bash

clean:
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf docs/api/*
	rm -rf docs/_build
	find . | grep -E "(__pycache__)" | xargs rm -rf

dist: clean
	@echo "Packaging module..."
	python -m pip install --upgrade build
	python -m build


publish-test: dist
	@echo "Packaging complete... Uploading to TEST instance of PyPi..."
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository test --sign dist/*


publish-live: dist
	@echo "Packaging complete... Uploading to LIVE instance of PyPi..."
	python3 -m pip install --upgrade twine
	python3 -m twine upload --sign dist/*
