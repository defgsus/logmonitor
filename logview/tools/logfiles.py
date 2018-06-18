import os
import gzip
import datetime


def load_logfiles(filename):
    path = os.path.dirname(filename)
    name = filename.split("/")[-1]
    filenames = []
    for root, dirs, files in os.walk(path):
        if root == path:
            for f in files:
                if f.startswith(name):
                    filenames.append(os.path.join(root, f))
    filenames.sort()

    all_data = []
    for fn in filenames:
        data = load_logfile(fn)
        all_data += data
    print(all_data)
    print(len(all_data))


def load_logfile(filename):
    dt = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    if filename.endswith(".gz"):
        with gzip.open(filename, "rt") as fp:
            return _load_logfile(fp, dt.year)
    else:
        with open(filename, "rt") as fp:
            return _load_logfile(fp, dt.year)


def _load_logfile(fp, year):
    ret = []
    lines = fp.read().split("\n")
    for line in lines:
        #print(line)
        if not line:
            continue
        if line[4] == " ":
            line = line[:4] + "0" + line[5:]
        dt = datetime.datetime.strptime(line[:15], "%b %d %H:%M:%S")
        dt = dt.replace(year=year)

        line = line[15:].split(":")
        user, task = line[0].strip().split(" ")
        text = ":".join(line[1:]).strip()

        ret.append({
            "date": dt,
            "user": user,
            "task": task,
            "text": text
        })
        #print(dt, user, task, text)
    return ret


if __name__ == "__main__":

    load_logfiles("/var/log/syslog")
