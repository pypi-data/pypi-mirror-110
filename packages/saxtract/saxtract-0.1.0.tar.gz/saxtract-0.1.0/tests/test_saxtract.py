#!/usr/bin/env python

"""Tests for `saxtract` package."""
from pathlib import Path

import pytest
from click.testing import CliRunner

from saxtract import cli


@pytest.fixture(autouse=True)
def runner():
    return CliRunner()


@pytest.fixture
def test_file_path():
    return (Path(__file__).parent / 'data' / 'bars.xml').absolute()


def test_cli_defaults(runner, test_file_path):
    """Test the CLI."""
    result = runner.invoke(cli.main, args=['--instream', f'{test_file_path}'])
    assert not result.exception
    assert result.exit_code == 0
