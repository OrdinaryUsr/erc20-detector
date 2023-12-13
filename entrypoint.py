from src.service import ERCService
from src.core.analyzers.analyzers import SlitherWrapper
from src.core.detectors.detectors import SignatureDetector
from src.core.constants.openzeppelin_erc20 import (
    ZEPPELIN_ERC20_ERRORS,
    ZEPPELIN_ERC20_EVENTS,
    ZEPPELIN_ERC20_FUNCTIONS,
)
from src.core.constants.openzeppelinv4_erc20 import (
    ZEPPELIN_V4_ERC20_EVENTS,
    ZEPPELIN_V4_ERC20_FUNCTIONS,
)
from src.core.constants.openzeppelinv3_erc20 import (
    ZEPPELIN_V3_ERC20_EVENTS,
    ZEPPELIN_V3_ERC20_FUNCTIONS,
)
from src.core.constants.openzeppelinv2_erc20 import (
    ZEPPELIN_V2_ERC20_EVENTS,
    ZEPPELIN_V2_ERC20_FUNCTIONS,
)
from src.storage.repository import ContractRepository
from src.app import Application
from src.storage.config import Session


def main() -> None:
    zeppelinv5_erc20_detector = SignatureDetector(
        ZEPPELIN_ERC20_FUNCTIONS, ZEPPELIN_ERC20_EVENTS, ZEPPELIN_ERC20_ERRORS
    )
    zeppelinv4_erc20_detector = SignatureDetector(
        ZEPPELIN_V4_ERC20_FUNCTIONS, ZEPPELIN_V4_ERC20_EVENTS, []
    )
    zeppelinv3_erc20_detector = SignatureDetector(
        ZEPPELIN_V3_ERC20_FUNCTIONS, ZEPPELIN_V3_ERC20_EVENTS, []
    )
    zeppelinv2_erc20_detector = SignatureDetector(
        ZEPPELIN_V2_ERC20_FUNCTIONS, ZEPPELIN_V2_ERC20_EVENTS, []
    )
    repository = ContractRepository(Session)
    service = ERCService(
        repository,
        SlitherWrapper,
        zeppelinv5_erc20_detector,
        zeppelinv4_erc20_detector,
        zeppelinv3_erc20_detector,
        zeppelinv2_erc20_detector,
    )
    application = Application(service)
    application.run()


if __name__ == "__main__":
    main()
