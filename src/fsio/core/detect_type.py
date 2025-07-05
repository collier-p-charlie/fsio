# -*- encode: utf-8 -*-

import logging
from io import BytesIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FileType:
    """
    Class to determine the file type of an object in **BytesIO** form.

    This is based on the _file signatures_ / _magic numbers_ as defined [here](https://en.wikipedia.org/wiki/List_of_file_signatures).
    """

    @classmethod
    def get_head_n_bytes(
        cls,
        body: BytesIO,
        n: int
    ) -> bytes:
        """
        Function to return the first `n` bytes from the **BytesIO** object.

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
        n: int
    ) -> bytes:
        """
        Function to return the last `n` bytes from the **BytesIO** object.

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
    def is_parquet(
        cls,
        body: BytesIO
    ) -> bool:
        """
        Function to determine if the provided **BytesIO** object is of **PARQUET** type or not.

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
                >>>
                >>> FileType.is_parquet(body)
                True
                ```
        """
        head4 = cls.get_head_n_bytes(body, 4)
        tail4 = cls.get_tail_n_bytes(body, 4)
        logger.debug(f"HEAD(4): {head4}")
        logger.debug(f"TAIL(4): {tail4}")
        return all(i == b'PAR1' for i in [head4, tail4])
