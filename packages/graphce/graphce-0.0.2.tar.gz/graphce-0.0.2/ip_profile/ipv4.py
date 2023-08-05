from ip_profile.ip_object import IpObject
from ip_profile.utils.ip_tree import IpTree
from ip_profile.utils.validator import Validator
from ip_profile.utils.common import to_number

validate = Validator.validate


class Ipv4(IpObject):
    def __init__(self, location):
        """
        Creates an object of :class:`ip_model.util.IpTree.IpTree`
        """
        self.head = IpTree(location)

    @validate
    def add(self, ip: str, info: str) -> bool:
        """
        Adds the given valid IPv4
        :param ip: An Ipv4 as String
        :returns: True for every new addition
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv4
        """
        num_ip = to_number(ip)
        self.head.add(num_ip, info)
        return True

    @validate
    def remove(self, ip) -> bool:
        """
        Removed the given valid IPv4
        :param ip: An Ipv4 as String
        :returns: str: The IP which is removed
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv4
        """
        num_ip = to_number(ip)
        self.head.remove(num_ip)
        return ip

    @validate
    def is_present(self, ip) -> bool:
        """
        Checks if a given valid IPv4 is present or not
        :param ip: An Ipv4 as String
        :returns: True, if the element is present
                  False, if the element is not present
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv4
        """
        num_ip = to_number(ip)
        return self.head.is_present(num_ip)

    @validate
    def update_ip_info(self, ip, info) -> bool:
        """
        Updates IP information.
        :param ip: An Ipv4 as String & score to update.
        :returns: False, if the entry doesn't exist.
                 True, if the entry exists & the score has been updated.
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv4
        """
        num_ip = to_number(ip)
        return self.head.update_ip_info(num_ip, info)
