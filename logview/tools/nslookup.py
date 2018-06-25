
import os
import datetime
import subprocess
from collections import OrderedDict

from ..models import NslookupRequest, WhoisRequest, DummyLogger


def get_nslookup_raw(ip, log=None, do_read_cache=True, do_write_cache=True, do_query=True):
    return _lookup_impl(
        NslookupRequest,
        ["nslookup", "%s" % ip],
        ip,
        log=log, do_read_cache=do_read_cache, do_write_cache=do_write_cache, do_query=do_query
    )


def get_nslookup(ip, log=None, do_read_cache=True, do_write_cache=True, do_query=True):
    ret = get_nslookup_raw(ip, log=log,
                           do_read_cache=do_read_cache, do_write_cache=do_write_cache, do_query=do_query)
    if ret is None:
        return ret
    if "\tname =" in ret:
        return ret.split("\tname =")[1].split()[0].strip(". ")
    return ret


def get_whois_raw(ip, log=None, do_read_cache=True, do_write_cache=True, do_query=True):
    return _lookup_impl(
        WhoisRequest,
        ["whois", "%s" % ip],
        ip,
        log=log, do_read_cache=do_read_cache, do_write_cache=do_write_cache, do_query=do_query
    )


def get_whois(ip, log=None, do_read_cache=True, do_write_cache=True, do_query=True):
    text = get_whois_raw(ip, log=log,
                         do_read_cache=do_read_cache, do_write_cache=do_write_cache, do_query=do_query)
    if text:
        dic = OrderedDict()
        for token in ("Organization:", "descr:", "netname:", "address:", "owner:"):
            if token in text:
                dic[token] = text.split(token)[1].split("\n")[0].strip()
        if dic:
            return " / ".join(dic.values())
    return text


def _lookup_impl(Model, args, ip, log=None, do_read_cache=True, do_write_cache=True, do_query=True):
    if do_read_cache:
        qset = Model.objects.filter(ip=ip)
        if qset.exists():
            return qset.order_by("-date")[0].response

    if not do_query:
        return None

    error = None
    try:
        res = subprocess.check_output(args, stderr=subprocess.STDOUT)
        res = res.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        error = e
        res = None
    except BaseException as e:
        error = e
        res = None

    if error is not None:
        if log is None:
            log = DummyLogger()
        log.error(error)

    if do_write_cache:
        Model.objects.create(
            date=datetime.datetime.now(),
            ip=ip,
            response=res,
        )
    return res


