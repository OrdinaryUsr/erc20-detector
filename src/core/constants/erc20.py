from src.core.signatures import FunctionSignature, EventSignature


ERC20_TRANSFER_EVENT = EventSignature(
    "Transfer", ["address", "address", "uint256"], [True, True, False]
)
ERC20_APPROVAL_EVENT = EventSignature(
    "Approval", ["address", "address", "uint256"], [True, True, False]
)
ERC20_EVENTS = [ERC20_TRANSFER_EVENT, ERC20_APPROVAL_EVENT]
ERC20_FUNCTIONS = [
    FunctionSignature("totalSupply", [], "uint256", True, []),
    FunctionSignature("balanceOf", ["address"], "uint256", True, []),
    FunctionSignature(
        "transfer", ["address", "uint256"], "bool", False, [ERC20_TRANSFER_EVENT]
    ),
    FunctionSignature(
        "transferFrom",
        ["address", "address", "uint256"],
        "bool",
        False,
        [ERC20_TRANSFER_EVENT],
    ),
    FunctionSignature(
        "approve", ["address", "uint256"], "bool", False, [ERC20_APPROVAL_EVENT]
    ),
    FunctionSignature("allowance", ["address", "address"], "uint256", True, []),
]
ERC20_EXTENDED_FUNCTIONS = ERC20_FUNCTIONS + [
    FunctionSignature("name", [], "string", True, []),
    FunctionSignature("symbol", [], "string", True, []),
    FunctionSignature("decimals", [], "uint8", True, []),
]
