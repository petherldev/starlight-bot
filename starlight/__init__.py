"""
Starlight-Bot package root.

Exposes:
    • __version__   – human-readable version string
    • pkg_resources – helper for reading data files bundled alongside code
"""

from importlib import resources as _resources

__all__: list[str] = ["__version__", "pkg_resources"]

__version__: str = "1.0.0"

# Just a thin re-export; useful if you ever embed templates / SQL / etc.
pkg_resources = _resources
