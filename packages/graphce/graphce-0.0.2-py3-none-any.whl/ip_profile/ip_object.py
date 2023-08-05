import abc


class IpObject:
    @abc.abstractmethod
    def add(self, ip: str, label: str):
        pass

    @abc.abstractmethod
    def remove(self, ip: str):
        pass

    @abc.abstractmethod
    def is_present(self, ip: str):
        pass

    @abc.abstractmethod
    def update_ip_info(self, ip: str, label: str):
        pass
