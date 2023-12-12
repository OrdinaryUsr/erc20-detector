from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from settings import POSTGRES_CONNECTION
from src.storage.models import Base, ContractModel


class ContractRepository:
    def __init__(self) -> None:
        self._engine = create_engine(POSTGRES_CONNECTION)
        Base.metadata.create_all(self._engine)

    def save(self, contract_model: ContractModel) -> None:
        with Session(self._engine) as session:
            session.add(contract_model)
            session.commit()

    def get_all(self) -> list[ContractModel]:
        session = Session(self._engine)
        stmt = select(ContractModel)
        return list(session.scalars(stmt))
