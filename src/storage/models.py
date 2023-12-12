from sqlalchemy import Column, Boolean, CHAR
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from src.status import ContractStatusEnum


Base = declarative_base()


class ContractModel(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_address: Mapped[str] = mapped_column(CHAR(50))
    source_code: Mapped[str]
    is_erc20: Mapped[bool] = mapped_column(Boolean(), default=False)
    erc20_version: Mapped[str] = mapped_column(CHAR(20), nullable=True)
    status: Mapped[str] = Column(
        PgEnum(
            ContractStatusEnum,
            name="contract_status_enum",
            create_type=True,
        ),
        nullable=False,
        default=ContractStatusEnum.WAITING,
    )
