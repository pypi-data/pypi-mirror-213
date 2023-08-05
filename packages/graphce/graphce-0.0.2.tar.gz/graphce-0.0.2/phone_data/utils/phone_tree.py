from typing import Tuple, Any

from phone_data.utils.phone_database_manipulation import PhoneDataManipulation

save_data = PhoneDataManipulation.save_data
remove_data = PhoneDataManipulation.remove_data
access_data = PhoneDataManipulation.access_data
save_updated_data = PhoneDataManipulation.save_updated_data


class Node:
    def __init__(self, data, children=None):
        self.data = data
        self.children = children if children is not None else {}


class PhoneTree:
    def __init__(self, location):
        self.head = Node("N")
        self.location = location

    def add(self, phone: str, info: dict):
        self._add_phone(self.head, phone, info, self.location)

    @save_data
    def _add_phone(self, head: str, phone: str, info: str, location: str) -> None:
        i = 0
        while i < len(phone):
            flag = False
            if len(head.data) > 1:
                for j, char in enumerate(head.data):
                    if char == phone[i + j - 1]:
                        continue
                    else:
                        split_node = Node(head.data[j:], head.children)
                        opp_char = head.data[j]
                        head.children[opp_char] = split_node
                        head.children[opp_char].info = head.info
                        head.data = head.data[:j]
                        head.children[phone[i + j - 1]] = Node(phone[i + j - 1:])
                        head.children[phone[i + j - 1]].info = info
                        flag = True
                        break
                i += j
                if i == len(phone) or flag:
                    break

            if i == len(phone):
                head.info = info
                return

            char = phone[i]
            if head.children.get(char) is None:
                head.children[char] = Node(phone[i:])
                head = head.children[char]
                break
            head = head.children[char]
            i += 1

        head.info = info
        return

    def remove(self, phone: str) -> bool:
        self._remove_phone(self.head, "N" + phone)

    @remove_data
    @access_data
    def _remove_phone(self, head, phone):
        i = 0
        prev_node = []
        root = head
        while i <= len(phone):
            if len(head.data) == 1:
                if phone[i] != head.data:
                    return False
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if phone[i + j] == bit:
                        continue
                    else:
                        return
                i += j
            if i == len(phone) - 1:
                prev_node[0].children[prev_node[1]] = "yes"
                return
            prev_node = [head, int(phone[i + 1])]
            if head.children[int(phone[i + 1])]:
                head = head.children[int(phone[i + 1])]
            else:
                return
            i += 1

    def is_present(self, phone: str) -> tuple[bool, int] | tuple[bool, Any]:
        return self._check_data(self.head, "N" + phone, self.location)

    @access_data
    def _check_data(self, head: str, phone: str, location: str) -> tuple[bool, int] | tuple[bool, Any]:
        i = 0
        # We iterate till 32 as we need to exclude the root node
        while i <= len(phone):
            if len(head.data) == 1:
                if phone[i] != head.data:
                    return False, -1
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if phone[i + j] != bit:
                        return False, -1
                i += j
            if i == len(phone) - 1:
                return True, head.info
            try:
                if head.children[phone[i + 1]]:
                    head = head.children[phone[i + 1]]
                else:
                    return False, -1
                i += 1
            except:
                return False, -1
        return True, head.info

    def update_phone_info(self, phone: str, info: dict) -> bool:
        return self._update_phone_info(self.head, "N" + phone, info, self.location)

    @save_updated_data
    def _update_phone_info(self, head: str, phone: str, info: dict, location: str) -> bool:
        i = 0
        root = head
        while i <= len(phone):
            if len(head.data) == 1:
                if phone[i] != head.data:
                    return False
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if phone[i + j] != bit:
                        return False
                i += j
            if i == len(phone) - 1:
                head.info = info
                return True
            if head.children[phone[i + 1]]:
                head = head.children[phone[i + 1]]
            else:
                return False
            i += 1
