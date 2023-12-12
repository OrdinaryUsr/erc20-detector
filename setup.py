from pathlib import Path
from shutil import copy
from solc_select.solc_select import (
    install_artifacts,
    artifact_path,
    get_available_versions,
)

from settings import SOLC_PATH
from src.storage.config import engine
from src.storage.models import Base


def install_solc():
    versions = get_available_versions()
    for version in versions:
        local_path = Path(f"{SOLC_PATH}solc-{version}")
        if local_path.exists():
            continue
        global_path = Path(artifact_path(version))
        if global_path.exists():
            copy(global_path, local_path)
            continue
        install_artifacts([version])
        copy(global_path, local_path)


def init_schema():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    install_solc()
    init_schema()
