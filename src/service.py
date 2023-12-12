from typing import Type

from src.core.analyzers.interfaces import IAnalyzer
from src.core.detectors.interfaces import IDetector
from src.storage.config import Session
from src.storage.repository import ContractRepository
from src.status import ContractStatusEnum


class ERCService:
    def __init__(
        self,
        repository_cls: Type[ContractRepository],
        analyzer_cls: Type[IAnalyzer],
        zeppelinv5_erc_detector: IDetector,
        zeppelinv4_erc_detector: IDetector,
        zeppelinv3_erc_detector: IDetector,
        zeppelinv2_erc_detector: IDetector,
    ) -> None:
        self._repository_cls = repository_cls
        self._analyzer_cls = analyzer_cls
        self._zeppelin_v5_detector = zeppelinv5_erc_detector
        self._zeppelin_v4_detector = zeppelinv4_erc_detector
        self._zeppelin_v3_detector = zeppelinv3_erc_detector
        self._zeppelin_v2_detector = zeppelinv2_erc_detector

    def contract_version(self, source_code: str) -> int | None:
        analyzer = self._analyzer_cls(source_code)
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
        with Session() as session:
            repo = self._repository_cls(session)
            contract_models = repo.lock_waiting_batch()
            for model in contract_models:
                version = self.contract_version(model.source_code)
                model.is_erc20 = bool(version)
                model.erc20_version = version
                model.status = ContractStatusEnum.DONE
                repo.save(model)
