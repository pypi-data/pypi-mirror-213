from typing import Tuple, Any

from email_data.utils.email_tree import EmailTree
from email_data.utils.validator import validator


class Email:
    def __init__(self, location):
        self.head = EmailTree(location)

    @validator
    def _add(self, email: str, info: str) -> bool:
        self.head.add(email, info)

    def _remove(self, email) -> bool:
        self.head.remove(email)
        return email

    @validator
    def _is_present(self, email) -> tuple[bool, int] | tuple[bool, Any]:
        return self.head.is_present(email)

    @validator
    def _update_info(self, email, info) -> bool:
        return self.head.update_email_info(email, info)
