from slither import Slither
from semver import Version

from src.analyzers.interfaces import IAnalyzer, IContract
from src.analyzers.contracts import SlitherContractWrapper
from src.analyzers.exceptions import InvalidSolidityVersion, CompilerFileDoesNotExist
from src.file_utils import create_solidity_file


class SlitherWrapper(IAnalyzer):
    def __init__(self, source_code: str) -> None:
        self._source_code = source_code
        self._version = self._parse_version()
        with create_solidity_file(self._source_code) as source_file:
            self._slither = Slither(source_file.name, solc="solc/solc-" + self._version)

    def _parse_version(self) -> str:
        # TODO: create parser class
        # TODO: cover more cases
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
