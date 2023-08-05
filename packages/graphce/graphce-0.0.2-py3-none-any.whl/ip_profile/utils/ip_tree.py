from ip_profile.utils.ip_data_manipulation import IPDataManipulation

save_data = IPDataManipulation.save_data
remove_data = IPDataManipulation.remove_data
access_data = IPDataManipulation.access_data
save_updated_data = IPDataManipulation.save_updated_data


class Node:
    def __init__(self, data, children=[None] * 10):
        self.data = data
        self.children = children


class IpTree:
    def __init__(self, location):
        self.head = Node("N")
        self.ip_loc = location

    def add(self, ip, info):
        self._add_ip(self.head, ip, info, self.ip_loc)

    @save_data
    def _add_ip(self, head, ip, info, location):
        i = 0
        while i <= len(ip):
            flag = False
            if len(head.data) > 1:
                for j, y in enumerate(head.data):
                    if y == ip[i + j - 1]:
                        # print ("1")
                        continue
                    else:
                        split_node = Node(head.data[j:], head.children)
                        index = int(ip[i + j - 1])
                        opp_index = int(head.data[j])
                        head.children = [None] * 10
                        head.children[opp_index] = split_node
                        head.children[opp_index].info = head.info
                        head.data = head.data[:j]
                        head.children[index] = Node(ip[i + j - 1:])
                        head.children[index].info = info
                        flag = True
                        break
                i += j
                if i == len(ip) or flag:
                    break
            if i == len(ip):
                head.info = info
                return
            child = int(ip[i])
            if head.children[child] is None:
                head.children[child] = Node(ip[i:])
                head = head.children[int(ip[i])]
                break
            head = head.children[int(ip[i])]
            i += 1

        head.info = info
        return

    def remove(self, ip) -> bool:
        self._remove_ip(self.head, "N" + ip)

    @remove_data
    @access_data
    def _remove_ip(self, head, ip):
        i = 0
        prev_node = []
        root = head
        while i <= len(ip):
            if len(head.data) == 1:
                if ip[i] != head.data:
                    return False
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if ip[i + j] == bit:
                        continue
                    else:
                        return
                i += j
            if i == len(ip) - 1:
                prev_node[0].children[prev_node[1]] = "yes"
                return
            prev_node = [head, int(ip[i + 1])]
            if head.children[int(ip[i + 1])]:
                head = head.children[int(ip[i + 1])]
            else:
                return
            i += 1

    def is_present(self, ip) -> bool:
        return self._check_data(self.head, "N" + ip, self.ip_loc)

    @access_data
    def _check_data(self, head, ip, location):
        i = 0
        while i <= len(ip):
            if len(head.data) == 1:
                if ip[i] != head.data:
                    return False, -1
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if ip[i + j] != bit:
                        return False, -1
                i += j
            if i == len(ip) - 1:
                return True, head.info
            if head.children[int(ip[i + 1])]:
                head = head.children[int(ip[i + 1])]
            else:
                return False, -1
            i += 1
        return True, head.info

    def update_info(self, ip, info="") -> bool:
        return self._update_ip_info(self.head, "N" + ip, info, self.ip_loc)

    @save_updated_data
    def _update_ip_info(self, head, ip, info, location):
        i = 0
        root = head
        while i <= len(ip):
            if len(head.data) == 1:
                if ip[i] != head.data:
                    return False
            elif len(head.data) > 1:
                for j, bit in enumerate(head.data):
                    if ip[i + j] != bit:
                        return False
                i += j
            if i == len(ip) - 1:
                head.info = info
                return True
            if head.children[int(ip[i + 1])]:
                head = head.children[int(ip[i + 1])]
            else:
                return False
            i += 1
