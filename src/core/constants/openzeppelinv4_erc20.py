from src.core.signatures import FunctionSignature
from src.core.constants.erc20 import (
    ERC20_EVENTS,
    ERC20_EXTENDED_FUNCTIONS,
    ERC20_TRANSFER_EVENT,
    ERC20_APPROVAL_EVENT,
)


ZEPPELIN_V4_ERC20_EVENTS = ERC20_EVENTS
ZEPPELIN_V4_ERC20_FUNCTIONS = ERC20_EXTENDED_FUNCTIONS + [
    FunctionSignature("constructor", ["string", "string"], None, False, []),
    FunctionSignature(
        "increaseAllowance",
        ["address", "uint256"],
        "bool",
        False,
        [ERC20_APPROVAL_EVENT],
    ),
    FunctionSignature(
        "decreaseAllowance",
        ["address", "uint256"],
        "bool",
        False,
        [ERC20_APPROVAL_EVENT],
    ),
    FunctionSignature(
        "_transfer",
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
        "_spendAllowance", ["address", "address", "uint256"], None, False, []
    ),
    FunctionSignature(
        "_beforeTokenTransfer", ["address", "address", "uint256"], None, False, []
    ),
    FunctionSignature(
        "_afterTokenTransfer", ["address", "address", "uint256"], None, False, []
    ),
]
