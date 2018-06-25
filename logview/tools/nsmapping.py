
from .nslookup import get_nslookup, get_whois


class NsMapping(object):

    def __init__(self):
        self._ip2url = dict()
        self._ip2owner = dict()

    def ip_to_url(self, ip):
        if ip not in self._ip2url:
            self._ip2url[ip] = get_nslookup(ip)
        return self._ip2url[ip]

    def ip_to_owner(self, ip):
        if ip not in self._ip2owner:
            self._ip2owner[ip] = get_whois(ip)
        return self._ip2owner[ip]

    def ip_decorator(self, ip):
        if not ip:
            return "-"
        ret = "%s" % ip
        url = self.ip_to_url(ip)
        if url:
            ret += " (<b>%s</b>)" % url

        owner = self.ip_to_owner(ip)
        if owner:
            ret += " (%s)" % owner

        return ret
