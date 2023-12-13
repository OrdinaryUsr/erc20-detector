from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src.storage.interfaces import IContractRepository
from src.storage.models import ContractModel
from src.status import ContractStatusEnum


class ContractRepository(IContractRepository):
    def __init__(self, session: sessionmaker[Session]) -> None:
        self._sessionmaker = session

    def save(self, model: ContractModel) -> None:
        with self._sessionmaker() as session:
            session.add(model)
            session.commit()

    def save_batch(self, models: list[ContractModel]) -> None:
        with self._sessionmaker() as session:
            session.add_all(models)
            session.commit()

    def get_all(self) -> list[ContractModel]:
        stmt = select(ContractModel)
        return list(self._sessionmaker().scalars(stmt))

    def lock_waiting_batch(self) -> list[ContractModel]:
        with self._sessionmaker() as session:
            stmt = (
                select(ContractModel)
                .filter_by(status=ContractStatusEnum.WAITING)
                .limit(5)
                .with_for_update()
            )
            models = list(session.scalars(stmt))
            for model in models:
                model.status = ContractStatusEnum.PROCESSING
                session.add(model)
            session.commit()
            return models
