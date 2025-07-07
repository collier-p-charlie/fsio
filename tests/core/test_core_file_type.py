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
        self.assertEqual(FileType.supported_types(), ['avro', 'bz2', 'gz', 'orc', 'parquet', 'xlsx', 'zip'])

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

    def test_is_avro_true(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertTrue(FileType.is_avro(body=self._get_file('avro')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'Obj\\x01'", logs.output)

    def test_is_avro_false(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertFalse(FileType.is_avro(body=self._get_file('csv')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'col1'", logs.output)

    def test_is_orc_true(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertTrue(FileType.is_orc(body=self._get_file('orc')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(3): b'ORC'", logs.output)

    def test_is_orc_false(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertFalse(FileType.is_orc(body=self._get_file('csv')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(3): b'col'", logs.output)

    def test_is_bz2_true(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertTrue(FileType.is_bz2(body=self._get_file('ext.bz2')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(3): b'BZh'", logs.output)

    def test_is_bz2_false(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertFalse(FileType.is_bz2(body=self._get_file('csv')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(3): b'col'", logs.output)

    def test_is_gz_true(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertTrue(FileType.is_gz(body=self._get_file('ext.gz')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(2): b'\\x1f\\x8b'", logs.output)

    def test_is_gz_false(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertFalse(FileType.is_gz(body=self._get_file('csv')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(2): b'co'", logs.output)

    def test_is_zip_true(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertTrue(FileType.is_zip(body=self._get_file('zip')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'PK\\x03\\x04'", logs.output)

    def test_is_zip_false(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertFalse(FileType.is_zip(body=self._get_file('csv')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'col1'", logs.output)

    def test_is_xlsx_true(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertTrue(FileType.is_xlsx(body=self._get_file('xlsx')))

        file_contents = {
            'xl/theme/theme1.xml',
            'docProps/app.xml',
            '[Content_Types].xml',
            'xl/worksheets/sheet1.xml',
            'xl/_rels/workbook.xml.rels',
            'xl/styles.xml',
            'xl/workbook.xml',
            'docProps/core.xml',
            '_rels/.rels'
        }
        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'PK\\x03\\x04'", logs.output)
        self.assertIn(f"INFO:{LOGGER_NAME}:Body is of ZIP type", logs.output)
        self.assertIn(f"DEBUG:{LOGGER_NAME}:ZIP file contents: {file_contents}", logs.output)

    def test_is_xlsx_false(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.DEBUG) as logs:
            self.assertFalse(FileType.is_xlsx(body=self._get_file('csv')))

        self.assertIn(f"DEBUG:{LOGGER_NAME}:HEAD(4): b'col1'", logs.output)

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
