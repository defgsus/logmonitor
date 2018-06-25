
from .nslookup import get_nslookup, get_whois


class NsMapping(object):

    def __init__(self):
        self._ip2url = dict()
        self._ip2owner = dict()
        self.do_read_cache = True
        self.do_write_cache = True
        self.do_query = True

    def ip_to_url(self, ip):
        if ip not in self._ip2url:
            self._ip2url[ip] = get_nslookup(
                ip, do_read_cache=self.do_read_cache, do_write_cache=self.do_write_cache, do_query=self.do_query)
        return self._ip2url[ip]

    def ip_to_owner(self, ip):
        if ip not in self._ip2owner:
            self._ip2owner[ip] = get_whois(
                ip, do_read_cache=self.do_read_cache, do_write_cache=self.do_write_cache, do_query=self.do_query)
        return self._ip2owner[ip]

    def ip_decorator(self, ip):
        if not ip:
            return "-"
        ret = ""

        url = self.ip_to_url(ip)
        if url:
            ret += "<br>(<b>%s</b>)" % url

        owner = self.ip_to_owner(ip)
        if owner:
            ret += "<br>(%s)" % owner

        if not ret:
            return ip

        ret = '%s<span class="ip-supplemental">%s</span>' % (ip, ret)
        return ret
