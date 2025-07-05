# -*- encode: utf-8 -*-

from io import BytesIO, TextIOWrapper
from unittest import TestCase

from src.fsio.core.detect_type import FileType


def _create_parquet_file(
    data: dict
) -> BytesIO:
    """
    :param data: dictionary with keys column names and values lists of data
        for example, {'col1': [1, 2], 'col2': ['a', 'b']}
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    table = pa.table(data)
    buffer = BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)

    return buffer


def _create_csv_file(
    data: dict
) -> BytesIO:
    """
    :param data: dictionary with keys column names and values lists of data
        for example, {'col1': [1, 2], 'col2': ['a', 'b']}
    """
    import csv

    buffer = BytesIO()
    text_stream = TextIOWrapper(buffer, encoding='utf-8', newline='\n')

    writer = csv.writer(text_stream)
    writer.writerows(zip(*(data[col] for col in data)))
    text_stream.flush()
    text_stream.detach()
    buffer.seek(0)

    return buffer


class TestCoreDetectType(TestCase):
    def test_get_head_n_bytes(self) -> None:
        body = BytesIO(b'ABCDE')
        self.assertEqual(FileType.get_head_n_bytes(body=body, n=3), b'ABC')

    def test_get_tail_n_bytes(self) -> None:
        body = BytesIO(b'ABCDE')
        self.assertEqual(FileType.get_tail_n_bytes(body=body, n=2), b'DE')

    def test_is_parquet_true(self) -> None:
        self.assertTrue(FileType.is_parquet(body=_create_parquet_file(data={'col1': [1]})))

    def test_is_parquet_false(self) -> None:
        self.assertFalse(FileType.is_parquet(body=_create_csv_file(data={'col1': [1]})))
