from ipaddress import ip_address, IPv4Address, ip_network
from ip_profile.ip_object import IpObject
from ip_profile.ipv4 import Ipv4
from ip_profile.ipv6 import Ipv6


class IP(IpObject):
    def __init__(self, location):
        self.ipv4 = Ipv4(location)
        self.ipv6 = Ipv6(location)

    def __ip_decider(self, ip: str):
        if isinstance(ip_address(ip), IPv4Address):
            return self.ipv4
        else:
            return self.ipv6

    def _add(self, ip: str, label: str):
        """
        Adds the given valid IP
        :param ip: An Ip as String
        :returns: True for every new addition
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IP
        """
        ipObject = self.__ip_decider(ip)
        return ipObject.add(ip, label)

    def _remove(self, ip: str):
        """
        Removed the given valid IP
        :param ip: An Ip as String
        :returns: str: The IP which is removed
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IP
        """
        ipObject = self.__ip_decider(ip)
        return ipObject.remove(ip)

    def _is_present(self, ip: str):
        """
        Checks if a given valid IP is present or not
        :param ip: An Ip as String
        :returns: True, if the element is present
                  False, if the element is not present
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IP
        """
        ipObject = self.__ip_decider(ip)
        return ipObject.is_present(ip)

    def _update_ip_info(self, ip: str, label: str):
        """
        Updates IP information.
        :param ip: An Ipv4 as String & score to update.
        :returns: False, if the entry doesn't exist.
                 True, if the entry exists & the score has been updated.
        :raises  :class:`ip_model.Exceptions.InvalidIpException` for invalid IPv4
        """
        ipObject = self.__ip_decider(ip)
        return ipObject.update_ip_info(ip, label)
