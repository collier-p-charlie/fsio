# -*- encode: utf-8 -*-

import logging
from io import BytesIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FileType:
    """
    Class to determine the file type of an object in BytesIO form.
    This is based on the file signatures / magic numbers as defined [here](https://en.wikipedia.org/wiki/List_of_file_signatures).
    """

    @classmethod
    def get_head_n_bytes(
        cls,
        body: BytesIO,
        n: int
    ) -> bytes:
        """
        Function to return the first N bytes from the BytesIO object.

        Args:
            body (io.BytesIO): the BytesIO object to extract the bytes from.
            n (int): the number of bytes to return.

        Returns:
            bytes: a bytes object containing the first N bytes of the data.

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
        n: int
    ) -> bytes:
        """
        Function to return the last N bytes from the BytesIO object.

        Args:
            body (io.BytesIO): the BytesIO object to extract the bytes from.
            n (int): the number of bytes to return.

        Returns:
            bytes: a bytes object containing the last N bytes of the data.

        Examples:
            >>> from io import BytesIO
            >>> FileType.get_head_n_bytes(BytesIO(b'Hello World!'), 6)
            b'World!'
        """
        body.seek(-n, 2)
        return body.read(n)

    @classmethod
    def is_parquet(
        cls,
        body: BytesIO
    ) -> bool:
        """
        Function to determine if the provided BytesIO object is of PARQUET type or not.

        Args:
            body (io.BytesIO): a BytesIO object containing the contents of the file to determine the type for.

        Returns:
            bool: a boolean True if the file is of PARQUET type or False if not.

        Examples:
            Basic usage::
                >>> from io import BytesIO
                >>> FileType.is_parquet(BytesIO(b'PAR1\x63\x68\x61\x7aPAR1'))
                True

            Explicit example::
                >>> from io import BytesIO
                >>> import pandas as pd
                >>>
                >>> body = BytesIO()
                >>> df = pd.DataFrame()
                >>> df.to_parquet(body)
                >>>
                >>> FileType.is_parquet(body)
                True
        """
        head4 = cls.get_head_n_bytes(body, 4)
        tail4 = cls.get_tail_n_bytes(body, 4)
        logger.debug(f"HEAD(4): {head4}")
        logger.debug(f"TAIL(4): {tail4}")
        return all(i == b'PAR1' for i in [head4, tail4])
