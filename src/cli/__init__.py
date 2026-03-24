"""Command line interface for SignalTrace CE.

This package exposes a user facing CLI that wraps the core
functionality of the SignalTrace CE project.  Commands include:

* ``validate`` – validates a synthetic dataset against the event schema.
* ``run`` – executes the full analysis pipeline and prints a summary.
* ``report-json`` – executes the pipeline and writes a JSON report.
* ``report-md`` – executes the pipeline and writes a Markdown report.
* ``summary`` – prints only the summary of the analysis to stdout.

Refer to ``docs/cli.md`` for detailed usage instructions.
"""

from .main import main  # noqa: F401
