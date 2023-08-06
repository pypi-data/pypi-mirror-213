# Climate Resource pre-commit hooks

<!--- sec-begin-description -->

[pre-commit](https://pre-commit.com/) hooks for ensuring consistency across our code
base. Included are hooks which are not available elsewhere and also not super useful
outside of a CR context.

<!--- sec-end-description -->

## Usage

<!--- sec-begin-usage -->

To use the hooks in a project, add to your `.pre-commit-config.yaml`:
```yaml
  - repo: https://gitlab.com/climate-resource/cr-pre-commit-hooks
    rev: v0.1.0
    hooks:
      - id: check-docstrings
```

<!--- sec-end-usage -->

## For developers

<!--- sec-begin-installation-dev -->

For development, we rely on [poetry](https://python-poetry.org) for all our
dependency management. To get started, you will need to make sure that poetry
is installed
([instructions here](https://python-poetry.org/docs/#installing-with-the-official-installer),
we found that pipx and pip worked better to install on a Mac).

For all of work, we use our `Makefile`.
You can read the instructions out and run the commands by hand if you wish,
but we generally discourage this because it can be error prone.
In order to create your environment, run `make virtual-environment`.

If there are any issues, the messages from the `Makefile` should guide you
through. If not, please raise an issue in the [issue tracker][issue_tracker].

For the rest of our developer docs, please see [](development-reference).

[issue_tracker]: https://gitlab.com/climate-resource/cr-pre-commit-hooks/issues

<!--- sec-end-installation-dev -->
