from src.core.signatures import FunctionSignature, ErrorSignature
from src.core.constants.erc20 import (
    ERC20_EVENTS,
    ERC20_EXTENDED_FUNCTIONS,
    ERC20_TRANSFER_EVENT,
    ERC20_APPROVAL_EVENT,
)


ZEPPELIN_ERC20_EVENTS = ERC20_EVENTS
ZEPPELIN_ERC20_ERRORS = [
    ErrorSignature("ERC20InsufficientBalance", ["address", "uint256", "uint256"]),
    ErrorSignature("ERC20InvalidSender", ["address"]),
    ErrorSignature("ERC20InvalidReceiver", ["address"]),
    ErrorSignature("ERC20InsufficientAllowance", ["address", "uint256", "uint256"]),
    ErrorSignature("ERC20InvalidApprover", ["address"]),
    ErrorSignature("ERC20InvalidSpender", ["address"]),
]
ZEPPELIN_ERC20_FUNCTIONS = ERC20_EXTENDED_FUNCTIONS + [
    FunctionSignature("constructor", ["string", "string"], None, False, []),
    FunctionSignature(
        "_transfer",
        ["address", "address", "uint256"],
        None,
        False,
        [ERC20_TRANSFER_EVENT],
    ),
    FunctionSignature(
        "_update",
        ["address", "address", "uint256"],
        None,
        False,
        [ERC20_TRANSFER_EVENT],
    ),
    FunctionSignature(
        "_mint", ["address", "uint256"], None, False, [ERC20_TRANSFER_EVENT]
    ),
    FunctionSignature(
        "_burn", ["address", "uint256"], None, False, [ERC20_TRANSFER_EVENT]
    ),
    FunctionSignature(
        "_approve",
        ["address", "address", "uint256"],
        None,
        False,
        [ERC20_APPROVAL_EVENT],
    ),
    FunctionSignature(
        "_approve",
        ["address", "address", "uint256", "bool"],
        None,
        False,
        [ERC20_APPROVAL_EVENT],
    ),
    FunctionSignature(
        "_spendAllowance", ["address", "address", "uint256"], None, False, []
    ),
]
