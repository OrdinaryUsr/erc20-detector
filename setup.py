from pathlib import Path
from shutil import copy
from solc_select.solc_select import (
    install_artifacts,
    artifact_path,
    get_available_versions,
)

from settings import SOLC_PATH


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


if __name__ == "__main__":
    install_solc()
