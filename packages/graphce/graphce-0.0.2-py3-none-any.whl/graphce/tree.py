"""
todo:
1. create a base class node for IPs
2. to showcase and display graphs we are creating(graphviz)
3. encryption and decryption
"""
# python level imports
from typing import Any

# project level libraries
from database.db_creation import DB_Creation
from ip_profile.ip import IP
from phone_data.phone import Phone
from email_data.email import Email
from edges.edge_manipulation import Edge


class GraphCE:
    def __init__(self, type_: str, location: str):
        """
        :param type_: type should be IP or PHONE or EMAIL (Uppercase)
        :param location: path of database as a string
        """
        self.__type = type_
        self.__location = f"{location}\\{type_}s.sqlite"
        self.__edge_location = f"{location}\\edges.sqlite"
        self.__edge = Edge(self.__edge_location)
        self.database = DB_Creation(self.__location, self.__edge_location)

        if self.__type == 'IP':
            self.__node_obj = IP(self.__location)
        elif self.__type == 'PHONE':
            self.__node_obj = Phone(self.__location)
        elif self.__type == 'EMAIL':
            self.__node_obj = Email(self.__location)
        else:
            raise TypeError("Invalid type")

    def add(self, value: str, info: dict) -> bool:
        """
        :param value: Phone number or IP address or Email
        :param info: information regarding value as a dict
        :return: True, if element is updated
                 False, if element is not updated
        """
        return self.__node_obj._add(value, info)

    def search(self, value: str) -> tuple[bool, int] | tuple[bool, Any]:
        """

        :param value: Phone number or IP address or Email
        :return: True and info, if element is present
                 False and -1, if element is not present
        """
        return self.__node_obj._is_present(value)

    def update(self, value: str, info: dict) -> bool:
        """

        :param value: Phone number or IP address or Email
        :param info: information regarding value as a dict
        :return: True, if element is updated
                 False, if element is not updated
        """
        return self.__node_obj._update_info(value, info)

    def create_edge(self, key: tuple, value: str) -> None:
        """

        :param key: Tuple of two nodes
        :param value: Information
        :return:
        """
        return self.__edge._create_edge(key, value)

    def access_edge(self, key: tuple) -> str:
        """

        :param key: Tuple of two nodes
        :return: value
        """
        return self.__edge._access_edge(key)

    def update_edge(self, key: tuple, value: str):
        """

        :param key: Tuple of two nodes
        :param value: Information
        :return:
        """
        return self.__edge._update_edge(key, value)

    def delete_edge(self, key: str):
        """

        :param key: Tuple of two nodes
        :return:
        """
        return self.__edge._delete_edge(key)