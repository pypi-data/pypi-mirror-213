from typing import Any

from email_data.utils.email_database_manipulation import EmailDataManipulation

save_data = EmailDataManipulation.save_data
remove_data = EmailDataManipulation.remove_data
access_data = EmailDataManipulation.access_data
save_updated_data = EmailDataManipulation.save_updated_data


class Node:
    def __init__(self, data, children=None):
        self.data = data
        self.children = children if children is not None else {}


class EmailTree:
    def __init__(self, location):
        self.head = Node("N")
        self.location = location

    def add(self, email, info):
        self._add_email(self.head, email, info, self.location)

    @save_data
    def _add_email(self, head: str, email: str, info: dict, location: str) -> bool | None:
        i = 0
        while i < len(email):
            flag = False
            if len(head.data) > 1:
                for j, char in enumerate(head.data):
                    if char == email[i + j - 1]:
                        continue
                    else:
                        split_node = Node(head.data[j:], head.children)
                        opp_char = head.data[j]
                        head.children[opp_char] = split_node
                        head.children[opp_char].info = head.info
                        head.data = head.data[:j]
                        head.children[email[i + j - 1]] = Node(email[i + j - 1:])
                        head.children[email[i + j - 1]].info = info
                        flag = True
                        break
                i += j
                if i == len(email) or flag:
                    break

            if i == len(email):
                head.info = info
                return
            char = email[i]
            if head.children.get(char) is None:
                head.children[char] = Node(email[i:])
                head = head.children[char]
                break
            head = head.children[char]
            i += 1

        head.info = info
        return True

    def remove(self, email) -> bool:
        self._remove_email(self.head, "N" + email)

    @remove_data
    @access_data
    def _remove_email(self, head, email):
        i = 0
        prev_node = []
        root = head
        while i <= len(email):
            if len(head.data) == 1:
                if email[i] != head.data:
                    return False
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if email[i + j] == bit:
                        continue
                    else:
                        return
                i += j
            if i == len(email) - 1:
                prev_node[0].children[prev_node[1]] = "yes"
                return
            prev_node = [head, int(email[i + 1])]
            if head.children[int(email[i + 1])]:
                head = head.children[int(email[i + 1])]
            else:
                return
            i += 1

    def is_present(self, email) -> tuple[bool, int] | tuple[bool, Any]:
        return self._check_data(self.head, "N" + email, self.location)

    @access_data
    def _check_data(self, head: str, email: str, location: str) -> tuple[bool, int] | tuple[bool, Any]:
        i = 0
        # We iterate till 32 as we need to exclude the root node
        while i <= len(email):
            if len(head.data) == 1:
                if email[i] != head.data:
                    return False, -1
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if email[i + j] != bit:
                        return False, -1
                i += j
            if i == len(email) - 1:
                return True, head.info
            try:
                if head.children[email[i + 1]]:
                    head = head.children[email[i + 1]]
                else:
                    return False, -1
                i += 1
            except:
                return False, -1
        return True, head.info

    def update_email_info(self, email, info="") -> bool:
        return self._update_email_info(self.head, "N" + email, info, self.location)

    @save_updated_data
    def _update_email_info(self, head: str, email: str, info: str, location: str) -> bool:
        i = 0
        root = head
        while i <= len(email):
            if len(head.data) == 1:
                if email[i] != head.data:
                    return False
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if email[i + j] != bit:
                        return False
                i += j
            if i == len(email) - 1:
                head.info = info
                return True
            if head.children[email[i + 1]]:
                head = head.children[email[i + 1]]
            else:
                return False
            i += 1
