# -*- encode: utf-8 -*-

from pathlib import Path

import pytest
from typer.testing import CliRunner

from fsio.cli.program import app

runner = CliRunner()


@pytest.fixture(scope="module")
def test_data_dir() -> Path:
    """Test data directory for this test class."""
    return Path(__file__).parent / "data"


class TestCliProgram:
    def test_supported_types(self) -> None:
        result = runner.invoke(app, ["supported-types"])

        assert result.exit_code == 0
        assert result.output.startswith("avro\nbz2\ngz\norc\nparquet\nxlsx\nxml\nzip")

    def test_detect_file_type_no_file_exists(self) -> None:
        file_path = "fake/path"
        result = runner.invoke(app, ["detect-file-type", file_path])

        assert result.exit_code == 1
        assert f"[ERROR] File not found: {file_path}" in result.output

    def test_detect_file_type_unknown_type(self, test_data_dir) -> None:
        file_path = test_data_dir / "example.ext"
        result = runner.invoke(app, ["detect-file-type", str(file_path)])

        assert result.exit_code == 0
        assert "File type could not be detected" in result.output

    def test_detect_file_type_parquet(self, test_data_dir) -> None:
        file_path = test_data_dir / "example.parquet"
        result = runner.invoke(app, ["detect-file-type", str(file_path)])

        assert result.exit_code == 0
        assert "parquet" in result.output
