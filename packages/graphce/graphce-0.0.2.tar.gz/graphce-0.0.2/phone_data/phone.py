from typing import Tuple, Any

from phone_data.utils.phone_tree import PhoneTree
from phone_data.utils.validator import validator


class Phone:
    def __init__(self, location):
        self.head = PhoneTree(location)

    @validator
    def _add(self, phone: str, info: str) -> str:
        self.head.add(phone, info)

    def _remove(self, phone) -> bool:
        self.head.remove(phone)
        return phone

    @validator
    def _is_present(self, phone) -> tuple[bool, int] | tuple[bool, Any]:
        return self.head.is_present(phone)

    @validator
    def _update_info(self, phone, info) -> bool:
        return self.head.update_phone_info(phone, info)
