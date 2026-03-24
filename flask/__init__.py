"""
Minimal stub of the Flask package for testing purposes.

This stub exists solely to satisfy type imports in the test suite.  It does not
provide any runtime functionality of the real Flask package.  Only
``FlaskClient`` is defined in the ``testing`` submodule to support type
annotations in tests.  If you need the full Flask features, install the
``flask`` package via pip.
"""

# Expose the testing submodule
from . import testing  # type: ignore[F401]

__all__ = ["testing"]
