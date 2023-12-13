import pytest

from src.core.analyzers.analyzers import SlitherWrapper
from src.core.detectors.detectors import SignatureDetector
from src.service import ERCService
from src.status import ContractStatusEnum
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
from src.storage.interfaces import IContractRepository
from src.storage.models import ContractModel


FILE_PREFIX = "tests/contracts/"


def read_source_file(name: str) -> str:
    with open(f"{FILE_PREFIX}{name}", mode="r", encoding="utf-8") as file:
        return file.read()


class InMemoryRepository(IContractRepository):
    def __init__(self) -> None:
        self._storage: dict[int, ContractModel] = {}

    def save(self, model: ContractModel) -> None:
        self._storage[model.id] = model

    def save_batch(self, models: list[ContractModel]) -> None:
        for model in models:
            self.save(model)

    def get(self, model_id: int) -> ContractModel:
        return self._storage[model_id]

    def get_all(self) -> list[ContractModel]:
        return list(self._storage.values())

    def lock_waiting_batch(self) -> list[ContractModel]:
        models: list[ContractModel] = []
        for _, value in self._storage.items():
            if value.status == ContractStatusEnum.WAITING:
                value.status = ContractStatusEnum.PROCESSING
                models.append(value)
        return models


class TestERCService:
    @pytest.fixture(scope="function")
    def zeppelin_v5_detector(self) -> SignatureDetector:
        return SignatureDetector(
            ZEPPELIN_ERC20_FUNCTIONS, ZEPPELIN_ERC20_EVENTS, ZEPPELIN_ERC20_ERRORS
        )

    @pytest.fixture(scope="function")
    def zeppelin_v4_detector(self) -> SignatureDetector:
        return SignatureDetector(
            ZEPPELIN_V4_ERC20_FUNCTIONS, ZEPPELIN_V4_ERC20_EVENTS, []
        )

    @pytest.fixture(scope="function")
    def zeppelin_v3_detector(self) -> SignatureDetector:
        return SignatureDetector(
            ZEPPELIN_V3_ERC20_FUNCTIONS, ZEPPELIN_V3_ERC20_EVENTS, []
        )

    @pytest.fixture(scope="function")
    def zeppelin_v2_detector(self) -> SignatureDetector:
        return SignatureDetector(
            ZEPPELIN_V2_ERC20_FUNCTIONS, ZEPPELIN_V2_ERC20_EVENTS, []
        )

    @pytest.fixture(scope="function")
    def repository(self) -> InMemoryRepository:
        return InMemoryRepository()

    @pytest.fixture(scope="function")
    def erc_service(
        self,
        repository: InMemoryRepository,
        zeppelin_v5_detector: SignatureDetector,
        zeppelin_v4_detector: SignatureDetector,
        zeppelin_v3_detector: SignatureDetector,
        zeppelin_v2_detector: SignatureDetector,
    ) -> ERCService:
        return ERCService(
            repository,
            SlitherWrapper,
            zeppelin_v5_detector,
            zeppelin_v4_detector,
            zeppelin_v3_detector,
            zeppelin_v2_detector,
        )

    @pytest.fixture(scope="function")
    def injectivetoken_model(self) -> ContractModel:
        return ContractModel(
            id=1,
            contract_address="injectivetoken",
            source_code=read_source_file("InjectiveToken.sol"),
            status=ContractStatusEnum.WAITING,
        )

    @pytest.fixture(scope="function")
    def shibainu_model(self) -> ContractModel:
        return ContractModel(
            id=1,
            contract_address="shibainu",
            source_code=read_source_file("ShibaInu.sol"),
            status=ContractStatusEnum.WAITING,
        )

    @pytest.fixture(scope="function")
    def zeppelin_model(self) -> ContractModel:
        return ContractModel(
            id=1,
            contract_address="zeppelin",
            source_code=read_source_file("ZeppelinERC20.sol"),
            status=ContractStatusEnum.WAITING,
        )

    @pytest.fixture(scope="function")
    def incorrectversion_model(self) -> ContractModel:
        return ContractModel(
            id=1,
            contract_address="incorrect",
            source_code=read_source_file("IncorrectVersion.sol"),
            status=ContractStatusEnum.WAITING,
        )

    @pytest.fixture(scope="function")
    def incorrectcompiler_model(self) -> ContractModel:
        return ContractModel(
            id=1,
            contract_address="incorrect",
            source_code=read_source_file("IncorrectCompiler.sol"),
            status=ContractStatusEnum.WAITING,
        )

    @pytest.fixture(scope="function")
    def incorrectsource_model(self) -> ContractModel:
        return ContractModel(
            id=1,
            contract_address="incorrect",
            source_code=read_source_file("data.txt"),
            status=ContractStatusEnum.WAITING,
        )

    def test_injectivetoken_erc20(
        self,
        erc_service: ERCService,
        repository: InMemoryRepository,
        injectivetoken_model: ContractModel,
    ) -> None:
        repository.save(injectivetoken_model)
        erc_service.process_batch()
        model = repository.get(injectivetoken_model.id)
        assert model.status == ContractStatusEnum.DONE
        assert model.is_erc20
        assert model.erc20_version == 3

    def test_shibainu_erc20(
        self,
        erc_service: ERCService,
        repository: InMemoryRepository,
        shibainu_model: ContractModel,
    ) -> None:
        repository.save(shibainu_model)
        erc_service.process_batch()
        model = repository.get(shibainu_model.id)
        assert model.status == ContractStatusEnum.DONE
        assert model.is_erc20
        assert model.erc20_version == 2

    def test_zeppelin_erc20(
        self,
        erc_service: ERCService,
        repository: InMemoryRepository,
        zeppelin_model: ContractModel,
    ) -> None:
        repository.save(zeppelin_model)
        erc_service.process_batch()
        model = repository.get(zeppelin_model.id)
        assert model.status == ContractStatusEnum.DONE
        assert model.is_erc20
        assert model.erc20_version == 5

    def test_incorrectversion_erc20(
        self,
        erc_service: ERCService,
        repository: InMemoryRepository,
        incorrectversion_model: ContractModel,
    ) -> None:
        repository.save(incorrectversion_model)
        erc_service.process_batch()
        model = repository.get(incorrectversion_model.id)
        assert model.status == ContractStatusEnum.FAILED
        assert not model.is_erc20
        assert not model.erc20_version

    def test_incorrectcompiler_erc20(
        self,
        erc_service: ERCService,
        repository: InMemoryRepository,
        incorrectcompiler_model: ContractModel,
    ) -> None:
        repository.save(incorrectcompiler_model)
        erc_service.process_batch()
        model = repository.get(incorrectcompiler_model.id)
        assert model.status == ContractStatusEnum.FAILED
        assert not model.is_erc20
        assert not model.erc20_version

    def test_incorrectsource_erc20(
        self,
        erc_service: ERCService,
        repository: InMemoryRepository,
        incorrectsource_model: ContractModel,
    ) -> None:
        repository.save(incorrectsource_model)
        erc_service.process_batch()
        model = repository.get(incorrectsource_model.id)
        assert model.status == ContractStatusEnum.FAILED
        assert not model.is_erc20
        assert not model.erc20_version
