# -*- encode: utf-8 -*-

import logging
import os
from io import BytesIO
from unittest import TestCase

from fsio.core.file_type import FileType

LOGGER_NAME = 'fsio.core.file_type'


class TestCoreDetectType(TestCase):
    def setUp(self) -> None:
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def _get_file(
        self,
        extension: str
    ) -> BytesIO:
        """
        Function to load the tests data file with the specified extension.
        """
        with open(os.path.join(self.test_data_dir, f'example.{extension}'), 'rb') as f:
            return BytesIO(f.read())

    def test_supported_types(self) -> None:
        self.assertEqual(FileType.supported_types(), ['parquet'])

    def test_get_head_n_bytes(self) -> None:
        body = BytesIO(b'ABCDE')
        self.assertEqual(FileType.get_head_n_bytes(body=body, n=3), b'ABC')

    def test_get_tail_n_bytes(self) -> None:
        body = BytesIO(b'ABCDE')
        self.assertEqual(FileType.get_tail_n_bytes(body=body, n=2), b'DE')

    def test_is_parquet_true(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertTrue(FileType.is_parquet(body=self._get_file('parquet')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'PAR1'", logs.output)
        self.assertIn(f"DEBUG:{LOGGER_NAME}:TAIL(4): b'PAR1'", logs.output)

    def test_is_parquet_false(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertFalse(FileType.is_parquet(body=self._get_file('csv')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'col1'", logs.output)
        self.assertIn(f"DEBUG:{LOGGER_NAME}:TAIL(4): b'\\n2,b'", logs.output)

    def test_detect_file_type_none(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.INFO) as logs:
            response = FileType.detect_file_type(BytesIO(b'UNKNOWN'))

        self.assertIsNone(response)

        supported_types = FileType.supported_types()
        self.assertIn(f'INFO:{LOGGER_NAME}:Body is not of any of the supported types: {supported_types}', logs.output)

    def test_detect_file_type_parquet(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            response = FileType.detect_file_type(self._get_file('parquet'))

        self.assertEqual(response, 'parquet')
        self.assertIn(f'DEBUG:{LOGGER_NAME}:Checking is_parquet(body)', logs.output)
