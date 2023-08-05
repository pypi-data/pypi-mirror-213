"""Checks for docstrings."""
import argparse
import ast
import collections.abc
import pathlib
import typing

import docstring_parser


def iter_docstrings(
    fname: typing.Union[str, pathlib.Path]
) -> collections.abc.Iterator[tuple[ast.FunctionDef, str]]:
    """Yield all function docstrings in the given file."""
    with open(fname) as fd:
        code = ast.parse(fd.read())
    for node in ast.walk(code):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if docstring:
                yield node, docstring


def docstring_returns_well_formed(
    docstring: str, fname: str, funcname: str, lineno: int
) -> str:
    """
    Check that if the docstring contains a "Returns" section, it is well formed.

    The rules are:
      * you need to have a description, which needs to be indented one level
      * you can have nothing else in the returns section, i.e. everything must be
        indented one level.

    If you want to specify a return name, the recommended format is to just have it
    at the start of the description followed by a full stop (see the Returns section
    of this function's docstring for an example).

    Parameters
    ----------
    docstring
        The docstring to check
    fname
        The file where the docstring was found, for building a useful error message
    funcname
        The name of the function in which the docstring was found
    lineno
        The line number where approximately the return definition was found

    Returns
    -------
        message. Error message if an error was found, otherwise empty string.
    """
    parsed = docstring_parser.parse(docstring, docstring_parser.DocstringStyle.NUMPYDOC)
    if parsed.returns is None:
        return ""
    if parsed.returns.type_name:
        msg = (
            "Name / type information exists - maybe description with missing"
            " indentation?"
        )
        return f'  File "{fname}", line {lineno} in {funcname}\n    {msg}'
    return ""


def main(argv: typing.Union[collections.abc.Sequence[str], None] = None) -> int:
    """
    Check docstrings in the given files.

    Parameters
    ----------
    argv
        Command line arguments

    Returns
    -------
        Return code
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        for node, docstring in iter_docstrings(filename):
            end_lineno_maybe_none = node.body[0].end_lineno
            if isinstance(end_lineno_maybe_none, int):
                end_lineno = end_lineno_maybe_none
            else:  # pragma: no cover
                end_lineno = 0
            msg = docstring_returns_well_formed(
                docstring,
                fname=filename,
                funcname=node.name,
                lineno=end_lineno - 1,
            )
            if msg:
                print(msg)
                retval = 1
    return retval


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
