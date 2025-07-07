# -*- encode: utf-8 -*-

import os
from unittest import TestCase

from typer.testing import CliRunner

from fsio.cli.program import app

runner = CliRunner()


class TestCliProgram(TestCase):
    def setUp(self) -> None:
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_supported_types(self) -> None:
        result = runner.invoke(app, ["supported-types"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(result.output.startswith('avro\nbz2\ngz\norc\nparquet\nxlsx\nzip'))

    def test_detect_file_type_no_file_exists(self) -> None:
        file_path = 'fake/path'
        result = runner.invoke(app, ["detect-file-type", file_path])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(f'[ERROR] File not found: {file_path}' in result.output)

    def test_detect_file_type_unknown_type(self) -> None:
        file_path = os.path.join(self.test_data_dir, 'example.ext')
        result = runner.invoke(app, ["detect-file-type", file_path])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue('File type could not be detected' in result.output)

    def test_detect_file_type_parquet(self) -> None:
        file_path = os.path.join(self.test_data_dir, 'example.parquet')
        result = runner.invoke(app, ["detect-file-type", file_path])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue('parquet' in result.output)
