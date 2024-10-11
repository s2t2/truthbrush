


build-docs:
	rm -rf docs/reference
	quartodoc build --config docs/_quarto.yml --verbose
	quarto render docs/
#	open docs/_build/index.html

open-docs:
	open docs/_build/index.html

preview-docs:
	rm -rf docs/reference
	quartodoc build --config docs/_quarto.yml
	quarto preview docs/
