# Notebook Convert pre commit hook [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[pre-commit hook](https://pre-commit.com/) for converting jupyter notebooks to multiple formats.

## Motivation

- ✅ Jupyter Notebooks are a great tool for doing data analysis

- ✅ You should treat them like code and keep them safe and available on a git repository

- ⚠️ Jupyter Notebooks format is not so great for doing __code reviews__ or PRs

- ⚠️ Jupyter Notebook default format is not the best for __communicating__ with less code-literate teams

## How to solve this with a commit hook

This commit hook does a couple of things for you:

- Lets you choose from a set of available __formats__ (currently Markdown, ReStructuredText and PDF)

- When committing your notebook, it __checks__ that it has an up to date companion format file

- If theres none, it __generates__ one for you

## Requirements

- A running [Docker](https://www.docker.com/) installation (generating different representations requires a lot of dependencies that are best encapsulated in a container)

## Installation

- Install [pre-commit](https://pre-commit.com/)

- Include _notebook convert_ as one of your hooks in your `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/fernandezpablo85/notebook_convert
    rev: <check latest release>
    hooks:
    -   id: notebook_convert
```

By default it will generate Markdown output, but you can also:

- Generate [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) files setting the `format` flag to `rst`

- Generate PDF files without input cells setting the `format` flag to `pdf`

For example:

```yaml
repos:
-   repo: https://github.com/fernandezpablo85/notebook_convert
    rev: <check latest release>
    hooks:
    -   id: notebook_convert
        args: [--format=pdf]
```

(If you want more than one representation just include the hook twice 🙃)

- Run `pre-commit install`

- Enjoy
