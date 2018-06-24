import os
import re
import gzip
import datetime


def load_logfiles(filename, file_id, after_date=None):
    path = os.path.dirname(filename)
    name = filename.split("/")[-1]
    filenames = []
    for root, dirs, files in os.walk(path):
        if root == path:
            for f in files:
                if f.startswith(name):
                    filenames.append(os.path.join(root, f))
    filenames.sort()

    if not filenames:
        print("not-found", filename)
        return []

    all_data = []
    for fn in filenames:
        data = load_logfile(fn, file_id)
        if after_date is None:
            all_data += data
        else:
            for d in data:
                if d["date"] > after_date:
                    all_data.append(d)
    return all_data


def load_logfile(filename, file_id):
    print("parse", filename)
    try:
        dt = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        if filename.endswith(".gz"):
            with gzip.open(filename, "rb") as fp:
                return _load_logfile(fp, file_id, filename, dt.year)
        else:
            with open(filename, "rb") as fp:
                return _load_logfile(fp, file_id, filename, dt.year)
    except PermissionError as e:
        print("permission-error", filename, e)
        return []
    except UnicodeDecodeError as e:
        print("unicode-error", filename, e)
        raise e
    except ValueError as e:
        print("value-error", filename, e)
        raise e


def _load_logfile(fp, file_id, filename, year):
    ret = []
    lines = fp.read()
    lines = lines.decode("utf-8").split("\n")

    num_no_date = 0
    num_errors = 0

    for line in lines:
        #print(line)
        if not line:
            continue

        source_ip = None

        if "nginx" in file_id:
            if "error" in file_id or "-error" in filename:
                dt = datetime.datetime.strptime(line[:19], "%Y/%m/%d %H:%M:%S")
                line = line[20:].strip()
                user = ""
                task = line[1:line.find("]")]
                text = line[line.find("]")+1:].strip()
            else:
                sline = line.split()
                if len(sline) < 5:
                    num_errors += 1
                    continue
                source_ip = sline[0]
                user = sline[1]
                dt = sline[3][1:]  # TODO: ignores timezone
                dt = datetime.datetime.strptime(dt, "%d/%b/%Y:%H:%M:%S")
                line = line[len(" ".join(sline[:5])):]
                line = line[line.find('"')+1:]
                task = line[0:line.find('"')]
                text = line[line.find('"')+1:]

        elif file_id == "dpkg":
            user = ""
            dt = datetime.datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
            line = line[20:].strip()
            sline = line.split()
            task = sline[0]
            text = " ".join(sline[1:])
        elif line.startswith("update-alternatives"):
            user = ""
            task = line[:20]
            line = line[20:]
            dt = datetime.datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
            text = line[20:].strip()
        else:
            if len(line) > 10:
                if line[4] == " ":
                    line = line[:4] + "0" + line[5:]

            try:
                dt = datetime.datetime.strptime(line[:15], "%b %d %H:%M:%S")
                date_len = 15
            except ValueError as e:
                try:
                    dt = datetime.datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
                    date_len = 19
                except ValueError as e:
                    num_no_date += 1
                    continue
            dt = dt.replace(year=year)

            line = line[date_len:]
            try:
                sline = line.split(":")
                user, task = sline[0].strip().split(" ")
                text = ":".join(sline[1:]).strip()
            except ValueError:
                user = ""
                sline = line.split(" ")
                task = sline[0]
                text = " ".join(sline[1:])

        ret.append(parse_entry({
            "date": dt,
            "user": user,
            "task": task,
            "text": text,
            "source_ip": source_ip,
        }))
        #print(dt, user, task, text)

    if num_no_date:
        print("parse-error", "%s without date" % num_no_date)
    if num_errors:
        print("parse-error", "%s general parse errors" % num_errors)
    return ret


def parse_entry(fields):
    text = fields.get("text", "")

    source_ip = None
    for ip in re.findall(r"SRC=(\d+\.\d+\.\d+\.\d+)", text):
        source_ip = ip

    for ip in re.findall(r"client: (\d+\.\d+\.\d+\.\d+)", text):
        source_ip = ip

    if source_ip:
        fields["source_ip"] = source_ip

    return fields


if __name__ == "__main__":

    if 0:
        after_date = datetime.datetime(2018, 6, 18, 10, 11, 58)
        data = load_logfiles("/var/log/syslog", "syslog", after_date=after_date)
        print(data)
        print(len(data))

    if 1:
        fields = {
            #"text": "[789990.372763] [UFW BLOCK] IN=enp3s0 OUT= MAC=c8:60:00:bc:3f:79:40:71:83:a2:fc:ae:08:00 SRC=5.188.10.103 DST=5.9.84.201 LEN=40 TOS=0x00 PREC=0x00 TTL=249 ID=58572 PROTO=TCP SPT=40731 DPT=2770 WINDOW=1024 RES=0x00 SYN URGP=0",
            "text": '2417#2417: *13839 open() "/srv/www/logmonitor/webrobots.txt" failed (2: No such file or directory), client: 66.249.66.218, server: _, request: "GET /robots.txt HTTP/1.1", host: "xn--80adhcckn5dbfh2ira.xn--p1ai"',
        }
        print(parse_entry(fields))
