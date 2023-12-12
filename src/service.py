from src.analyzers.interfaces import IAnalyzer
from src.detectors.interfaces import IDetector


class ERCService:
    def __init__(
        self,
        analyzer_cls: type(IAnalyzer),
        erc20_detector: IDetector,
        zeppelin_erc20_detector: IDetector,
    ) -> None:
        self._analyzer_cls = analyzer_cls
        self._erc20_detector = erc20_detector
        self._zeppelin_erc20_detector = zeppelin_erc20_detector

    def check_erc20(self, source_code: str) -> bool:
        analyzer = self._analyzer_cls(source_code)
        return self._erc20_detector.detect(analyzer)

    def check_zeppelin_erc20(self, source_code: str) -> bool:
        analyzer = self._analyzer_cls(source_code)
        return self._zeppelin_erc20_detector.detect(analyzer)
