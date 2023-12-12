from enum import Enum


class ContractStatusEnum(Enum):
    WAITING = "WAITING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"
