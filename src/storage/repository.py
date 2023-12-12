from sqlalchemy import select
from sqlalchemy.orm import Session

from src.storage.models import ContractModel


class ContractRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, contract_model: ContractModel) -> None:
        self._session.add(contract_model)
        self._session.commit()

    def get_all(self) -> list[ContractModel]:
        stmt = select(ContractModel)
        return list(self._session.scalars(stmt))
