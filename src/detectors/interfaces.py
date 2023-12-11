from abc import ABC, abstractmethod

from src.analyzers.interfaces import IAnalyzer


class IDetector(ABC):
    @abstractmethod
    def detect(self, analyzer: IAnalyzer) -> bool:
        pass
