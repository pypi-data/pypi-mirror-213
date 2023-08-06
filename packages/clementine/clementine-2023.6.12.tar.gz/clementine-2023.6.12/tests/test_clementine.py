"""Tests for clementine."""

from clementine.about import __version__


def test_version():
  assert __version__ == '2023.6.12'
