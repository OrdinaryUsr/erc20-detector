from abc import ABC, abstractmethod

from src.core.analyzers.interfaces import IAnalyzer


class IDetector(ABC):
    @abstractmethod
    def detect(self, analyzer: IAnalyzer) -> bool:
        pass
