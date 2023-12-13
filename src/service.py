from typing import Type

from src.core.analyzers.interfaces import IAnalyzer
from src.core.analyzers.exceptions import InvalidSolidityVersion, CompilationError
from src.core.detectors.interfaces import IDetector
from src.storage.interfaces import IContractRepository
from src.status import ContractStatusEnum


class ERCService:
    def __init__(
        self,
        repository: IContractRepository,
        analyzer_cls: Type[IAnalyzer],
        zeppelinv5_erc_detector: IDetector,
        zeppelinv4_erc_detector: IDetector,
        zeppelinv3_erc_detector: IDetector,
        zeppelinv2_erc_detector: IDetector,
    ) -> None:
        self._repository = repository
        self._analyzer_cls = analyzer_cls
        self._zeppelin_v5_detector = zeppelinv5_erc_detector
        self._zeppelin_v4_detector = zeppelinv4_erc_detector
        self._zeppelin_v3_detector = zeppelinv3_erc_detector
        self._zeppelin_v2_detector = zeppelinv2_erc_detector

    def contract_version(self, analyzer: IAnalyzer) -> int | None:
        if self._zeppelin_v5_detector.detect(analyzer):
            return 5
        if self._zeppelin_v4_detector.detect(analyzer):
            return 4
        if self._zeppelin_v3_detector.detect(analyzer):
            return 3
        if self._zeppelin_v2_detector.detect(analyzer):
            return 2
        return None

    def process_batch(self) -> None:
        contract_models = self._repository.lock_waiting_batch()
        for model in contract_models:
            try:
                analyzer = self._analyzer_cls(model.source_code)
            except (InvalidSolidityVersion, CompilationError):
                model.mark_as_failed()
                continue
            version = self.contract_version(analyzer)
            model.is_erc20 = bool(version)
            model.erc20_version = version
            model.status = ContractStatusEnum.DONE
        self._repository.save_batch(contract_models)
