pypi: build upload

build:
	@echo "Building package..."
	@pip install --upgrade build twine
	@python -m build

upload:
	@echo "Uploading package..."
	@python -m twine upload --repository pypi dist/*

install:
	@echo "Building editable package..."
	@pip install -e .
