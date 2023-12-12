from src.detectors.interfaces import IDetector
from src.analyzers.interfaces import IAnalyzer, IContract
from src.entities.signatures import FunctionSignature, EventSignature, ErrorSignature


class SignatureDetector(IDetector):
    def __init__(
        self,
        functions: list[FunctionSignature],
        events: list[EventSignature],
        errors: list[ErrorSignature],
    ) -> None:
        self._functions = functions
        self._events = events
        self._errors = errors

    def _check_functions(self, contract: IContract) -> bool:
        for signature in self._functions:
            if not contract.check_function(signature):
                return False
        return True

    def _check_events(self, contract: IContract) -> bool:
        for signature in self._events:
            if not contract.check_event(signature):
                return False
        return True

    def _check_errors(self, contract: IContract) -> bool:
        for signature in self._errors:
            if not contract.check_error(signature):
                return False
        return True

    def detect(self, analyzer: IAnalyzer) -> bool:
        for contract in analyzer.contracts:
            if (
                self._check_functions(contract)
                and self._check_events(contract)
                and self._check_errors(contract)
            ):
                return True
        return False
