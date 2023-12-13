from abc import ABC, abstractmethod

from src.storage.models import ContractModel


class IContractRepository(ABC):
    @abstractmethod
    def save(self, model: ContractModel) -> None:
        pass

    @abstractmethod
    def save_batch(self, models: list[ContractModel]) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[ContractModel]:
        pass

    @abstractmethod
    def lock_waiting_batch(self) -> list[ContractModel]:
        pass
