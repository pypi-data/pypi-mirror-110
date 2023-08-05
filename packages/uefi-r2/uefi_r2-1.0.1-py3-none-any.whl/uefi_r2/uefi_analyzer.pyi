from typing import Any, Dict, List, Optional
from uefi_r2.uefi_protocols import GUID_FROM_BYTES as GUID_FROM_BYTES, UefiGuid as UefiGuid
from uefi_r2.uefi_tables import BS_PROTOCOLS_INFO_64_BIT as BS_PROTOCOLS_INFO_64_BIT, EFI_BOOT_SERVICES_64_BIT as EFI_BOOT_SERVICES_64_BIT, EFI_PEI_SERVICES_32_BIT as EFI_PEI_SERVICES_32_BIT, EFI_RUNTIME_SERVICES_64_BIT as EFI_RUNTIME_SERVICES_64_BIT, OFFSET_TO_SERVICE as OFFSET_TO_SERVICE
from uefi_r2.uefi_te import TerseExecutableError as TerseExecutableError, TerseExecutableParser as TerseExecutableParser

class UefiService:
    name: Any = ...
    address: Any = ...
    def __init__(self, name: str, address: int) -> None: ...
    @property
    def __dict__(self): ...

class UefiProtocol(UefiGuid):
    address: Any = ...
    guid_address: Any = ...
    service: Any = ...
    def __init__(self, name: str, address: int, value: str, guid_address: int, service: str) -> None: ...
    @property
    def __dict__(self): ...

class UefiProtocolGuid(UefiGuid):
    address: Any = ...
    def __init__(self, name: str, address: int, value: str) -> None: ...
    @property
    def __dict__(self): ...

class NvramVariable:
    name: Any = ...
    guid: Any = ...
    service: Any = ...
    def __init__(self, name: str, guid: str, service: UefiService) -> None: ...
    @property
    def __dict__(self): ...

class UefiAnalyzer:
    def __init__(self, image_path: Optional[str]=..., radare2home: Optional[str]=...) -> None: ...
    @property
    def info(self) -> List[Any]: ...
    @property
    def strings(self) -> List[Any]: ...
    @property
    def sections(self) -> List[Any]: ...
    @property
    def functions(self) -> List[Any]: ...
    @property
    def insns(self) -> List[Any]: ...
    @property
    def g_bs(self) -> int: ...
    @property
    def g_rt(self) -> int: ...
    @property
    def boot_services(self) -> List[UefiService]: ...
    @property
    def boot_services_protocols(self) -> List[Any]: ...
    @property
    def runtime_services(self) -> List[UefiService]: ...
    @property
    def protocols(self) -> List[UefiProtocol]: ...
    @property
    def protocol_guids(self) -> List[UefiProtocolGuid]: ...
    def r2_get_nvram_vars_64_bit(self) -> List[NvramVariable]: ...
    @property
    def nvram_vars(self) -> List[NvramVariable]: ...
    @property
    def pei_services(self) -> List[UefiService]: ...
    @property
    def ppi_list(self) -> List[UefiProtocol]: ...
    @classmethod
    def get_summary(cls, image_path: str) -> Dict[str, Any]: ...
    @classmethod
    def get_protocols_info(cls, image_path: str) -> Dict[str, Any]: ...
    def close(self) -> None: ...
    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None: ...
