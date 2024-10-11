# Truthbrush Documentation Site

## Prerequisites

### Quarto

The documentation site is built using [Quarto](https://quarto.org/). Quarto can be [downloaded](https://quarto.org/docs/get-started/), or [installed via homebrew](https://formulae.brew.sh/cask/quarto) (if you like that kind of thing):

```sh
brew install --cask quarto
```

If you use VS Code, you can also consider installing the [Quarto Extension](https://marketplace.visualstudio.com/items?itemName=quarto.quarto).


## Docs Environment

Setup environment and install package dependencies:

```sh
conda create -n truthbrush-docs python=3.10
conda activate truthbrush-docs

conda install -c conda-forge poetry
poetry install --with docs
```



## Auto Documentation

In the "quartodoc" section of the ["_quarto.yml" config file](/docs/_quarto.yml), we specify that our site should display "references/index.qmd", which acts as the entrypoint into the package auto-documentation.

We are using [quartodoc](https://machow.github.io/quartodoc/get-started/basic-docs.html) to automatically generate docstring content into the "docs/references" directory:

```sh
quartodoc build --config docs/_quarto.yml --verbose
```

After the documentation pages have been generated, then we can preview and build the site.


## Building


Previewing the site (runs like a local webserver):

```sh
quarto preview docs/
```


Rendering the site (writes local HTML files to the "docs/_build" directory, which is ignored from version control):

```sh
quarto render docs/ --verbose
```


### Website Publishing

We are using the ["quarto-pages.yml" workflow configuration file](/.github/workflows/quarto-pages.yml) to deploy the site to GitHub Pages when new commits are pushed to the main branch.

In order for this to work, the GitHub Pages repo settings need to be configured to publish via GitHub Actions.
