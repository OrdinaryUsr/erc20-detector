from dataclasses import dataclass


@dataclass
class ErrorSignature:
    name: str
    parameters: list[str]


@dataclass
class EventSignature:
    name: str
    parameters: list[str]
    indexes: list[bool]


@dataclass
class FunctionSignature:
    name: str
    parameters: list[str]
    return_type: str | None
    view: bool
    events: list[EventSignature]
