class InvalidSolidityVersion(Exception):
    def __init__(self, version: str) -> None:
        self.version = version
        self.message = f'Invalid solidity version "{version}"'
        super().__init__()


class CompilerFileDoesNotExist(Exception):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.message = f'No such compiler "{file_path}"'
        super().__init__()
