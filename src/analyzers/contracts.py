from slither.core.declarations import Contract, Function
from slither.slithir.operations import EventCall

from src.analyzers.interfaces import IContract
from src.entities.signatures import FunctionSignature, EventSignature, ErrorSignature


class SlitherContractWrapper(IContract):
    def __init__(self, contract: Contract) -> None:
        self._contract = contract

    def _check_function_return_type(
        self, function: Function, signature: FunctionSignature
    ) -> bool:
        if function.return_type:
            return_type_string = ",".join([str(x) for x in function.return_type])
            if return_type_string != signature.return_type:
                return False
        elif signature.return_type:
            return False
        return True

    def _check_function_events(
        self, function: Function, signature: FunctionSignature
    ) -> bool:
        for event in signature.events:
            event_found = False
            for ir in function.all_slithir_operations():
                if (
                    isinstance(ir, EventCall)
                    and ir.name == event.name
                    and event.parameters == [str(a.type) for a in ir.arguments]
                ):
                    event_found = True
                    break
            return event_found
        return True

    def check_function(self, signature: FunctionSignature) -> bool:
        signature_string = f'{signature.name}({",".join(signature.parameters)})'
        function = self._contract.get_function_from_signature(signature_string)
        if not function or function.view != signature.view:
            return False
        if not self._check_function_return_type(function, signature):
            return False
        if signature.events and not self._check_function_events(function, signature):
            return False
        return True

    def check_event(self, signature: EventSignature) -> bool:
        signature_string = f'{signature.name}({",".join(signature.parameters)})'
        event = self._contract.get_event_from_signature(signature_string)
        if not event:
            return False
        for i, index in enumerate(signature.indexes):
            if index and not event.elems[i].indexed:
                return False
        return True

    def check_error(self, signature: ErrorSignature) -> bool:
        signature_string = f'{signature.name}({",".join(signature.parameters)})'
        error = self._contract.custom_errors_as_dict.get(signature.name)
        if not error:
            return False
        return signature_string == error.solidity_signature

    @property
    def name(self) -> str:
        return self._contract.name
