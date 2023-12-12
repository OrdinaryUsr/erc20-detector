from sqlalchemy import Column, Boolean, CHAR, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from src.status import ContractStatusEnum


Base = declarative_base()


class ContractModel(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_address: Mapped[str] = mapped_column(CHAR(50))
    source_code: Mapped[str]
    is_erc20: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    erc20_version: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[ContractStatusEnum] = Column(
        PgEnum(
            ContractStatusEnum,
            name="contract_status_enum",
            create_type=True,
        ),
        nullable=False,
        default=ContractStatusEnum.WAITING,
    )
