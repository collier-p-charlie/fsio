# -*- encode: utf-8 -*-

import logging
import re
from io import BytesIO
from pathlib import Path

import pytest

from fsio.core.file_type import FileType

LOGGER_NAME = "fsio.core.file_type"


@pytest.fixture(scope="module")
def test_data_dir() -> Path:
    """Test data directory for this test class."""
    return Path(__file__).parent / "data"


def get_file(extension: str, test_data_dir: Path) -> BytesIO:
    """Function to load the tests data file with the specified extension."""
    path = Path(test_data_dir, f"example.{extension}")
    with path.open(mode="rb") as f:
        return BytesIO(f.read())


class TestCoreDetectType:
    def test_supported_types(self) -> None:
        assert FileType.supported_types() == [
            "avro",
            "bz2",
            "gz",
            "orc",
            "parquet",
            "xlsx",
            "xml",
            "zip",
        ]

    def test_get_head_n_bytes(self) -> None:
        assert FileType.get_head_n_bytes(body=BytesIO(b"ABCDE"), n=3) == b"ABC"

    def test_get_tail_n_bytes(self) -> None:
        assert FileType.get_tail_n_bytes(body=BytesIO(b"ABCDE"), n=2) == b"DE"

    def test_is_xml_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_xml(body=get_file("xml", test_data_dir))

        assert response
        assert "HEAD(6): b'<?xml '" in caplog.text

    def test_is_xml_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_xml(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(6): b'col1,c'" in caplog.text

    def test_is_parquet_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_parquet(body=get_file("parquet", test_data_dir))

        assert response
        assert "HEAD(4): b'PAR1'" in caplog.text
        assert "TAIL(4): b'PAR1'" in caplog.text

    def test_is_parquet_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_parquet(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(4): b'col1'" in caplog.text
        assert "TAIL(4): b'2,b\\n'" in caplog.text

    def test_is_avro_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_avro(body=get_file("avro", test_data_dir))

        assert response
        assert "HEAD(4): b'Obj\\x01'" in caplog.text

    def test_is_avro_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_avro(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(4): b'col1'" in caplog.text

    def test_is_orc_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_orc(body=get_file("orc", test_data_dir))

        assert response
        assert "HEAD(3): b'ORC'" in caplog.text

    def test_is_orc_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_orc(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(3): b'col'" in caplog.text

    def test_is_bz2_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_bz2(body=get_file("ext.bz2", test_data_dir))

        assert response
        assert "HEAD(3): b'BZh'" in caplog.text

    def test_is_bz2_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_bz2(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(3): b'col'" in caplog.text

    def test_is_gz_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_gz(body=get_file("ext.gz", test_data_dir))

        assert response
        assert "HEAD(2): b'\\x1f\\x8b'" in caplog.text

    def test_is_gz_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_gz(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(2): b'co'" in caplog.text

    def test_is_zip_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_zip(body=get_file("zip", test_data_dir))

        assert response
        assert "HEAD(4): b'PK\\x03\\x04'" in caplog.text

    def test_is_zip_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_zip(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(4): b'col1'" in caplog.text

    def test_is_xlsx_true(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_xlsx(body=get_file("xlsx", test_data_dir))

        assert response
        assert "HEAD(4): b'PK\\x03\\x04'" in caplog.text
        assert re.search("INFO.*Body is of ZIP type", caplog.text)
        assert "ZIP file contents" in caplog.text

        file_contents = {
            "xl/theme/theme1.xml",
            "docProps/app.xml",
            "[Content_Types].xml",
            "xl/worksheets/sheet1.xml",
            "xl/_rels/workbook.xml.rels",
            "xl/styles.xml",
            "xl/workbook.xml",
            "docProps/core.xml",
            "_rels/.rels",
        }

        for file_type in file_contents:
            assert file_type in caplog.text

    def test_is_xlsx_false(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.is_xlsx(body=get_file("csv", test_data_dir))

        assert not response
        assert "HEAD(4): b'col1'" in caplog.text

    def test_detect_file_type_none(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.detect_file_type(body=get_file("ext", test_data_dir))

        assert response is None
        assert (
            f"Body is not of any of the supported types: {FileType.supported_types()}"
            in caplog.text
        )

    def test_detect_file_type_parquet(self, caplog, test_data_dir) -> None:
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            response = FileType.detect_file_type(body=get_file("parquet", test_data_dir))

        assert response == "parquet"
        assert "Checking is_parquet(body)" in caplog.text
