from slither import Slither
from slither.slither import SlitherError
from semver import Version

from settings import SOLC_PATH
from src.core.analyzers.interfaces import IAnalyzer, IContract
from src.core.analyzers.contracts import SlitherContractWrapper
from src.core.analyzers.exceptions import (
    InvalidSolidityVersion,
    CompilationError,
)
from src.core.file_utils import create_solidity_file


class SlitherWrapper(IAnalyzer):
    def __init__(self, source_code: str) -> None:
        self._source_code = source_code
        self._version = self._parse_version()
        with create_solidity_file(self._source_code) as source_file:
            path = f"{SOLC_PATH}solc-{self._version}"
            try:
                self._slither = Slither(source_file.name, solc=path)
            except SlitherError as e:
                raise CompilationError(path) from e

    def _parse_version(self) -> str:
        version_lines = filter(
            lambda line: line.strip(" ").startswith("pragma solidity"),
            self._source_code.split("\n"),
        )
        version_line = next(version_lines, "")
        if not version_lines:
            raise InvalidSolidityVersion("version not found")
        version = version_line.split(" ")[-1].strip(";^<>=")
        try:
            Version.parse(version)
        except ValueError as e:
            raise InvalidSolidityVersion(version) from e
        return version_line.split(" ")[-1].strip(";^<>=")

    @property
    def contracts(self) -> list[IContract]:
        return [SlitherContractWrapper(x) for x in self._slither.contracts]

    @property
    def version(self) -> str:
        return self._version
