#coding: utf-8

__auther__ = "xiaohuahu94@gmail.com"

from requests import get as r_get
from lxml import etree

PROXY_FILE_PATH = 'ips.txt'

class IPPool(object):
    def __init__(self, file_path, req_per_proxy=1000):
        self.ips = self._get_ips_from_file(file_path); assert type(self.ips) == list
        self.ip_dict = {}
        for ip in self.ips:
            self.ip_dict[ip] = 0
        self.req_per_proxy = req_per_proxy

    def get_an_ip(self):
        for ip in self.ip_dict.keys(): # 先返回已经有次数且在设定范围内的
            if self.ip_dict[ip] in range(1, self.req_per_proxy):
                self.ip_dict[ip] += 1
                return ip

        for ip in self.ip_dict.keys(): # 都无次数，返回有效的ip
            if self.ip_dict[ip] == 0:
                if not self._validate_ip(ip):
                    print 'invalid proxy: {}'.format(ip)
                    self.ip_dict[ip] = -1 # -1标记无效ip, 所有ip跑完后清空
                    continue
                self.ip_dict[ip] += 1
                return ip

        for ip in self.ip_dict.keys(): # 所有ip次数满，清零后返回
            self.ip_dict[ip] = 0

        return self.get_an_ip() 

    def _get_ips_from_file(self, file_path):
        ips = []
        with open(file_path, 'r') as f:
            for line in f.readlines():
                ips.append(line.strip())
        return ips

    def _validate_ip(self, ip):
        proxy = {'http':ip,
                'https':ip}
        try:
            resp = r_get('https://www.google.com', timeout=5, proxies=proxy)
        except Exception as ee:
            return False
        
        return bool(resp.status_code == 200) 

if __name__ == '__main__':
    pool1 = IPPool(file_path=PROXY_FILE_PATH, req_per_proxy=1000)
    for _ in range(1000):
        print 'get a valid ip: {}'.format(pool1.get_an_ip())

