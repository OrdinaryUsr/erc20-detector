from src.service import ERCService
from src.core.analyzers.analyzers import SlitherWrapper
from src.core.detectors.detectors import SignatureDetector
from src.core.constants.erc20 import ERC20_EVENTS, ERC20_FUNCTIONS
from src.core.constants.openzeppelin_erc20 import (
    ZEPPELIN_ERC20_ERRORS,
    ZEPPELIN_ERC20_EVENTS,
    ZEPPELIN_ERC20_FUNCTIONS,
)
from src.storage.repository import ContractRepository
from src.app import Application


def main() -> None:
    erc20_detector = SignatureDetector(ERC20_FUNCTIONS, ERC20_EVENTS, [])
    zeppelin_erc20_detector = SignatureDetector(
        ZEPPELIN_ERC20_FUNCTIONS, ZEPPELIN_ERC20_EVENTS, ZEPPELIN_ERC20_ERRORS
    )
    service = ERCService(SlitherWrapper, erc20_detector, zeppelin_erc20_detector)
    application = Application(service, ContractRepository)
    application.run()


if __name__ == "__main__":
    main()
