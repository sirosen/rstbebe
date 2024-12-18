.PHONY: build
build:
	pipx run build .

.PHONY: publish
publish: build
	pipx run twine upload dist/*
