from ip_profile.ip_object import IpObject
from ip_profile.utils.ip_tree import IpTree
from ip_profile.utils.validator import Validator
from ip_profile.utils.common import to_number

validate = Validator.validate_ipv6

class Ipv6(IpObject):
    def __init__(self, location):
        self.head = IpTree(location)

    @validate
    def add(self, ip: str, label: str) -> bool:
        """
        Adds the given valid IPv6
        :param ip: An IPv6 as String
        :returns: True for every new addition
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv6
        """
        num_ip = to_number(ip)
        self.head.add(num_ip, label)
        return True

    @validate
    def remove(self, ip) -> bool:
        """
        Removed the given valid IPv6
        :param ip: An IPv6 as String
        :returns: str: The IP which is removed
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv6
        """
        num_ip = to_number(ip)
        self.head.remove(num_ip)
        return ip

    @validate
    def is_present(self, ip) -> bool:
        """
        Checks if a given valid IPv6 is present or not
        :param ip: An Ipv4 as String
        :returns: True, if the element is present
                  False, if the element is not present
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv6
        """
        num_ip = to_number(ip)
        return self.head.is_present(num_ip)
    
    @validate
    def update_ip_info(self, ip, score) -> bool:
        """
        Updates IP information. 
        :param ip: An Ipv6 as String & score to update.
        :returns: False, if the entry doesn't exist.
                 True, if the entry exists & the score has been updated.
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv6
        """
        num_ip = to_number(ip)
        return self.head.update_ip_info(num_ip, score)