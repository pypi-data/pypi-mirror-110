from typing import Any, Dict

class UefiGuid:
    value: Any = ...
    name: Any = ...
    def __init__(self, value: str, name: str) -> None: ...
    @property
    def bytes(self) -> bytes: ...
    @property
    def __dict__(self): ...

PROTOCOLS_GUIDS: Any
GUID_FROM_VALUE: Dict[str, UefiGuid]
GUID_FROM_BYTES: Dict[bytes, UefiGuid]
