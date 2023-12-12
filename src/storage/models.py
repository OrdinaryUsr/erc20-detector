from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from src.statuses import ContractStatusEnum


class Base(DeclarativeBase):
    pass


class ContractModel(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_address: Mapped[str] = mapped_column(String(50))
    source_code: Mapped[str]
    is_erc20: Mapped[bool] = mapped_column(Boolean(), default=False)
    erc20_version: Mapped[str] = mapped_column(String(), nullable=True)
    status: Mapped[str] = Column(
        PgEnum(
            ContractStatusEnum,
            name="contract_status_enum",
            create_type=True,
        ),
        nullable=False,
        default=ContractStatusEnum.WAITING,
    )
