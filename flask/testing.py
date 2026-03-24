"""
Testing utilities stub for the Flask package.

This module defines a minimal ``FlaskClient`` type used in the test suite to
annotate the type of a test client.  The actual implementation of the client
is provided by the application under test (see ``src/api/server.py``).  This
stub avoids importing the real Flask library, which is not available in the
community edition environment.
"""

from typing import Any


class FlaskClient:
    """
    Placeholder class for Flask's test client.

    This class intentionally has no implementation.  Its presence allows
    test modules to import :class:`FlaskClient` from ``flask.testing`` for
    type annotations without requiring the real Flask dependency.

    Instances returned by the API's ``test_client`` method may not be
    instances of this class, but the annotation does not affect runtime
    behaviour.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass
