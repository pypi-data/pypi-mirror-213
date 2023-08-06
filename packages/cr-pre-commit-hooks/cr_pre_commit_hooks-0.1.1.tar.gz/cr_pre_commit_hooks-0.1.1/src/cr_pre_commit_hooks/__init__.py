"""
pre-commit hooks for ensuring consistency across our code base.

Included are hooks which are not available elsewhere and also
not super useful outside of a CR context.
"""
import importlib.metadata

__version__ = importlib.metadata.version("cr_pre_commit_hooks")
