from abc import ABC, abstractmethod

from src.core.signatures import FunctionSignature, EventSignature, ErrorSignature


class IContract(ABC):
    @abstractmethod
    def check_function(self, signature: FunctionSignature) -> bool:
        pass

    @abstractmethod
    def check_event(self, signature: EventSignature) -> bool:
        pass

    @abstractmethod
    def check_error(self, signature: ErrorSignature) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class IAnalyzer(ABC):
    @property
    @abstractmethod
    def contracts(self) -> list[IContract]:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass
