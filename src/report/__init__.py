"""Reporting utilities for SignalTrace CE.

This package contains helper functions to generate structured
reports and user‑friendly summaries.  Reports are based solely on
synthetic data processed by the SignalTrace CE pipeline.  Use
:func:`generate_analysis_result` to produce a JSON serialisable
analysis result and :func:`generate_markdown_report` to turn that
result into a human‑readable Markdown document.

The report generator functions rely on the same internal modules
utilised by the API and CLI, ensuring consistency across different
interfaces.
"""

from .generator import generate_analysis_result, generate_markdown_report  # noqa: F401
