import pytest

from src.analyzers.analyzers import SlitherWrapper
from src.detectors.detectors import SignatureDetector
from src.service import ERCService
from src.constants.erc20 import ERC20_FUNCTIONS, ERC20_EVENTS
from src.constants.openzeppelin_erc20 import (
    ZEPPELIN_ERC20_FUNCTIONS,
    ZEPPELIN_ERC20_EVENTS,
    ZEPPELIN_ERC20_ERRORS,
)


FILE_PREFIX = "tests/contracts/"


class TestERCService:
    @pytest.fixture(scope="class")
    def erc20_detector(self) -> SignatureDetector:
        return SignatureDetector(ERC20_FUNCTIONS, ERC20_EVENTS, [])

    @pytest.fixture(scope="class")
    def zeppelin_erc20_detector(self) -> SignatureDetector:
        return SignatureDetector(
            ZEPPELIN_ERC20_FUNCTIONS, ZEPPELIN_ERC20_EVENTS, ZEPPELIN_ERC20_ERRORS
        )

    @pytest.fixture(scope="class")
    def erc_service(
        self,
        erc20_detector: SignatureDetector,
        zeppelin_erc20_detector: SignatureDetector,
    ) -> ERCService:
        return ERCService(SlitherWrapper, erc20_detector, zeppelin_erc20_detector)

    def test_injectivetoken_erc20(self, erc_service: ERCService) -> None:
        with open(
            f"{FILE_PREFIX}InjectiveToken.sol", mode="r", encoding="utf-8"
        ) as file:
            src = file.read()
        assert erc_service.check_erc20(src)

    def test_shibainu_erc20(self, erc_service: ERCService) -> None:
        with open(f"{FILE_PREFIX}ShibaInu.sol", mode="r", encoding="utf-8") as file:
            src = file.read()
        assert erc_service.check_erc20(src)

    def test_zeppelin_erc20(self, erc_service: ERCService) -> None:
        with open(
            f"{FILE_PREFIX}ZeppelinERC20.sol", mode="r", encoding="utf-8"
        ) as file:
            src = file.read()
        assert erc_service.check_erc20(src)
