# -*- encode: utf-8 -*-

import inspect
import logging
import zipfile
from io import BytesIO
from types import MethodType

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FileType:
    """Class to determine the file type of an object in **BytesIO** form.

    This is based on the _file signatures_ / _magic numbers_ as defined [here](https://en.wikipedia.org/wiki/List_of_file_signatures).
    """

    @classmethod
    def supported_types(
        cls,
    ) -> list[str]:
        """Function to return the current supported types for _file detection_.
        This is determined from the current `@classmethod` objects of the form `is_<type>`.

        Returns:
            A **list** of **str** objects containing the supported types.

        Examples:
            >>> FileType.supported_types()
            ['avro', 'bz2', 'gz', 'orc', 'parquet', 'xlsx', 'xml', 'zip']
        """
        return sorted(
            attr.lstrip("is_")
            for attr in dir(cls)
            if isinstance(inspect.getattr_static(cls, attr), classmethod) and attr.startswith("is_")
        )

    @classmethod
    def get_detection_methods(
        cls,
    ) -> list[MethodType]:
        """Function to return the current supported _file detection_ methods.

        Returns:
            A **list** of `@classmethod` detection methods.

        Examples:
            >>> FileType.get_detection_methods()
        """
        return [getattr(cls, f"is_{s_type}") for s_type in cls.supported_types()]

    @classmethod
    def get_head_n_bytes(
        cls,
        body: BytesIO,
        n: int,
    ) -> bytes:
        """Function to return the first `n` bytes from the **BytesIO** object.

        Args:
            body: The **BytesIO** object to extract the bytes from.
            n: The number of **bytes** to return.

        Returns:
            A `bytes` object containing the first `n` bytes of the data.

        Examples:
            >>> from io import BytesIO
            >>> FileType.get_head_n_bytes(BytesIO(b'Hello World!'), 5)
            b'Hello'
        """
        body.seek(0)
        return body.read(n)

    @classmethod
    def get_tail_n_bytes(
        cls,
        body: BytesIO,
        n: int,
    ) -> bytes:
        """Function to return the last `n` bytes from the **BytesIO** object.

        Args:
            body: The **BytesIO** object to extract the bytes from.
            n: The number of **bytes** to return.

        Returns:
            A **bytes** object containing the last `n` bytes of the data.

        Examples:
            >>> from io import BytesIO
            >>> FileType.get_tail_n_bytes(BytesIO(b'Hello World!'), 6)
            b'World!'
        """
        body.seek(-n, 2)
        return body.read(n)

    @classmethod
    def is_xml(
        cls,
        body: BytesIO,
    ) -> bool:
        r"""Function to determine if the provided **BytesIO** object is of **XML** type or not.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **XML** type or `False` if not.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.is_xml(BytesIO(b'<?xml\x20\x63\x68\x61\x7aPAR1'))
                True
                ```

            Explicit example
                ```python
                >>> from io import BytesIO
                >>> import xml.etree.ElementTree as ET
                >>>
                >>> body = BytesIO()
                >>> root = ET.Element('data')
                >>> tree = ET.ElementTree(root)
                >>> tree.write(body, encoding='utf-8', xml_declaration=True)
                >>> body.seek(0)
                >>>
                >>> FileType.is_xml(body)
                True
                ```
        """
        head6 = cls.get_head_n_bytes(body, 6)
        logger.debug("HEAD(6): %r", head6)
        return head6 == b"<?xml\x20"

    @classmethod
    def is_parquet(
        cls,
        body: BytesIO,
    ) -> bool:
        r"""Function to determine if the provided **BytesIO** object is of **PARQUET** type or not.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **PARQUET** type or `False` if not.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.is_parquet(BytesIO(b'PAR1\x63\x68\x61\x7aPAR1'))
                True
                ```

            Explicit example
                ```python
                >>> from io import BytesIO
                >>> import pandas as pd
                >>>
                >>> body = BytesIO()
                >>> df = pd.DataFrame()
                >>> df.to_parquet(body)
                >>> body.seek(0)
                >>>
                >>> FileType.is_parquet(body)
                True
                ```
        """
        head4 = cls.get_head_n_bytes(body, 4)
        tail4 = cls.get_tail_n_bytes(body, 4)
        logger.debug("HEAD(4): %r", head4)
        logger.debug("TAIL(4): %r", tail4)
        return all(i == b"PAR1" for i in [head4, tail4])

    @classmethod
    def is_avro(
        cls,
        body: BytesIO,
    ) -> bool:
        r"""Function to determine if the provided **BytesIO** object is of **AVRO** type or not.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **AVRO** type or `False` if not.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.is_avro(BytesIO(b'Obj\x01\x63\x68\x61\x7a'))
                True
                ```

            Explicit example
                ```python
                >>> from io import BytesIO
                >>> import pandas as pd
                >>> from fastavro import writer
                >>>
                >>> body = BytesIO()
                >>> df = pd.DataFrame(columns=["age"], data=[[18]])
                >>> schema = {"type": "record", "name": "ages", "fields": [{"name": "age", "type": "int"}]}
                >>> writer(body, schema, df.to_dict(orient="records"))
                >>> body.seek(0)
                >>>
                >>> FileType.is_avro(body)
                True
                ```
        """
        head4 = cls.get_head_n_bytes(body, 4)
        logger.debug("HEAD(4): %r", head4)
        return head4 == b"Obj\x01"

    @classmethod
    def is_orc(
        cls,
        body: BytesIO,
    ) -> bool:
        r"""Function to determine if the provided **BytesIO** object is of **ORC** type or not.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **ORC** type or `False` if not.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.is_orc(BytesIO(b'ORC\x63\x68\x61\x7a'))
                True
                ```

            Explicit example
                ```python
                >>> from io import BytesIO
                >>> import pandas as pd
                >>>
                >>> body = BytesIO()
                >>> df = pd.DataFrame()
                >>> df.to_orc(body)
                >>> body.seek(0)
                >>>
                >>> FileType.is_orc(body)
                True
                ```
        """
        head3 = cls.get_head_n_bytes(body, 3)
        logger.debug("HEAD(3): %r", head3)
        return head3 == b"ORC"

    @classmethod
    def is_bz2(
        cls,
        body: BytesIO,
    ) -> bool:
        r"""Function to determine if the provided **BytesIO** object is of **BZ2** compression type or not.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **BZ2** compression type or `False` if not.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.is_bz2(BytesIO(b'BZh\x63\x68\x61\x7a'))
                True
                ```

            Explicit example
                ```python
                >>> import bz2
                >>> from io import BytesIO
                >>>
                >>> body = BytesIO()
                >>> with bz2.BZ2File(body, 'wb') as f:
                >>>     f.write(b'\x63\x68\x61\x7a')
                >>>
                >>> body.seek(0)
                >>> FileType.is_bz2(body)
                True
                ```
        """
        head3 = cls.get_head_n_bytes(body, 3)
        logger.debug("HEAD(3): %r", head3)
        return head3 == b"BZh"

    @classmethod
    def is_gz(
        cls,
        body: BytesIO,
    ) -> bool:
        r"""Function to determine if the provided **BytesIO** object is of **GZIP** compression type or not.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **GZIP** compression type or `False` if not.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.is_gz(BytesIO(b'\x1f\x8b\x63\x68\x61\x7a'))
                True
                ```

            Explicit example
                ```python
                >>> import gzip
                >>> from io import BytesIO
                >>>
                >>> body = BytesIO()
                >>> with gzip.GzipFile(fileobj=body, mode="wb") as f:
                >>>     f.write(b'\x63\x68\x61\x7a')
                >>>
                >>> body.seek(0)
                >>> FileType.is_gz(body)
                True
                ```
        """
        head2 = cls.get_head_n_bytes(body, 2)
        logger.debug("HEAD(2): %r", head2)
        return head2 == b"\x1f\x8b"

    @classmethod
    def is_zip(
        cls,
        body: BytesIO,
    ) -> bool:
        r"""Function to determine if the provided **BytesIO** object is of **ZIP** compression type or not.
        Note that this also includes types such as `.docx` and `.xlsx`.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **ZIP** compression type or `False` if not.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.is_zip(BytesIO(b'PK\x03\x04\x63\x68\x61\x7a'))
                True
                ```

            Explicit example
                ```python
                >>> import zipfile
                >>> from io import BytesIO
                >>>
                >>> body = BytesIO()
                >>> with zipfile.ZipFile(body, 'w') as zip:
                >>>     zip.writestr('file.ext', b'\x63\x68\x61\x7a')
                >>>
                >>> body.seek(0)
                >>> FileType.is_zip(body)
                True
                ```
        """
        head4 = cls.get_head_n_bytes(body, 4)
        logger.debug("HEAD(4): %r", head4)
        return any(head4 == i for i in [b"PK\x03\x04", b"PK\x05\x06", b"PK\x08\x08"])

    @classmethod
    def is_xlsx(
        cls,
        body: BytesIO,
    ) -> bool:
        """Function to determine if the provided **BytesIO** object is of **XLSX** type or not.

        Args:
            body: A **BytesIO** object containing the contents of the file to determine the type for.

        Returns:
            A boolean `True` if the file is of **XLSX** type or `False` if not.

        Examples:
            >>> from pathlib import Path
            >>> from io import BytesIO
            >>>
            >>> body = BytesIO()
            >>> excel_path = Path('path/to/excel.xlsx')
            >>> with excel_path.open('rb') as f:
            >>>     body.write(f.read())
            >>>
            >>> body.seek(0)
            >>> FileType.is_xlsx(body)
            True
        """
        if cls.is_zip(body):
            logger.info("Body is of ZIP type")
            # https://en.wikipedia.org/wiki/Office_Open_XML#Standardization_process
            required_files = {
                "[Content_Types].xml",
                "_rels/.rels",
                "xl/workbook.xml",
                "xl/_rels/workbook.xml.rels",
                "xl/worksheets/sheet1.xml",
            }
            with zipfile.ZipFile(body, "r") as zip_file:
                file_contents = set(zip_file.namelist())
                logger.debug("ZIP file contents: %s", file_contents)
                if required_files.issubset(file_contents):
                    return True

        return False

    @classmethod
    def detect_file_type(
        cls,
        body: BytesIO,
    ) -> str | None:
        r"""Function to detect the _file type_ of the provided **BytesIO** object.

        Args:
            body: The **BytesIO** object to determine the _file type_ of.

        Returns:
            A **str** containing the name of the _file type_.

        Examples:
            Basic usage
                ```python
                >>> from io import BytesIO
                >>> FileType.detect_file_type(BytesIO(b'PAR1\x63\x68\x61\x7aPAR1'))
                'parquet'
                ```

            Unsupported type usage
                ```python
                >>> from io import BytesIO
                >>> FileType.detect_file_type(BytesIO(b'\x63\x68\x61\x7a'))
                None
                ```
        """
        for method in cls.get_detection_methods():
            logger.debug("Checking %s(body)", method.__name__)
            if method(body=body):
                return method.__name__.lstrip("is_")

        supported_types = cls.supported_types()
        logger.info("Body is not of any of the supported types: %s", supported_types)
        return None
