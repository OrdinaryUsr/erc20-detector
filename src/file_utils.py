from typing import Generator, IO
from contextlib import contextmanager
import tempfile


@contextmanager
def create_solidity_file(source: str) -> Generator[IO[str], None, None]:
    file = tempfile.NamedTemporaryFile(mode="r+", suffix=".sol")
    file.write(source)
    file.seek(0)
    try:
        yield file
    finally:
        file.close()
