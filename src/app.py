import time

from src.service import ERCService
from src.storage.repository import ContractRepository
from src.status import ContractStatusEnum
from src.storage.config import Session


class Application:
    def __init__(
        self, service: ERCService, repository_cls: type(ContractRepository)
    ) -> None:
        self._service = service
        self._repository_cls = repository_cls

    def run(self) -> None:
        while True:
            try:
                with Session() as session:
                    repo = self._repository_cls(session)
                    contract_models = repo.lock_waiting_batch()
                    for model in contract_models:
                        model.is_erc20 = self._service.check_erc20(model.source_code)
                        model.status = ContractStatusEnum.DONE
                        repo.save(model)
                time.sleep(1)
            except KeyboardInterrupt:
                break
