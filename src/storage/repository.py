from sqlalchemy import select
from sqlalchemy.orm import Session

from src.storage.models import ContractModel
from src.status import ContractStatusEnum


class ContractRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, model: ContractModel) -> None:
        self._session.add(model)
        self._session.commit()

    def get_all(self) -> list[ContractModel]:
        stmt = select(ContractModel)
        return list(self._session.scalars(stmt))

    def lock_waiting_batch(self) -> list[ContractModel]:
        stmt = (
            select(ContractModel)
            .filter_by(status=ContractStatusEnum.WAITING)
            .limit(5)
            .with_for_update()
        )
        models = list(self._session.scalars(stmt))
        for model in models:
            model.status = ContractStatusEnum.PROCESSING
            self._session.add(model)
        self._session.commit()
        return models
