from src.core.analyzers.interfaces import IAnalyzer
from src.core.detectors.interfaces import IDetector


class ERCService:
    def __init__(
        self,
        analyzer_cls: type(IAnalyzer),
        erc_detector: IDetector,
        zeppelin_erc_detector: IDetector,
    ) -> None:
        self._analyzer_cls = analyzer_cls
        self._erc_detector = erc_detector
        self._zeppelin_erc_detector = zeppelin_erc_detector

    def check_erc20(self, source_code: str) -> bool:
        analyzer = self._analyzer_cls(source_code)
        return self._erc_detector.detect(analyzer)

    def check_zeppelin_erc20(self, source_code: str) -> bool:
        analyzer = self._analyzer_cls(source_code)
        return self._zeppelin_erc_detector.detect(analyzer)
