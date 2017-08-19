#!/usr/bin/env python2

from __future__ import print_function
import socket, sys, re, json, shutil
from termcolor import colored

if len(sys.argv) != 4:
    print("Usage %s port channel outdir" % (sys.argv[0]))
    print("e.g. %s 9000 @mychannel $(mktemp -d)" % (sys.argv[0]))
    sys.exit(-1)


def sendRecv(s, command):
    s.sendall(command + " \n")
    n = 1024
    first = True
    data = ""
    while len(data) < n:
        packet = s.recv(n - len(data))
        if not packet:
            break
        if first:
            c = packet.split("\n", 1)
            n = int(next(iter(re.findall("ANSWER (\d+)", c[0]) or []), None)) + 1
            packet = c[1]
            first = False
        data += packet
    return data


outdir = sys.argv[3]
code = -1
host = 'localhost'
port = int(sys.argv[1])
channel = sys.argv[2]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    print("Getting messages ... ", end='')
    sys.stdout.flush()

    messages = []
    photos = []
    s.connect((host, port))
    offset = 0
    while offset >= 0:
        command = b"history %s %d %d" % (channel, 100, offset)
        data = json.loads(sendRecv(s, command), strict=False)
        messages.extend(data)
        print("\rGetting messages ... ", end='')
        print(colored("%d" % len(messages), 'yellow'), end='')
        sys.stdout.flush()
        if len(data):
            offset += 100
        else:
            offset = -1
    print(colored(" [done] ", "green"))
    for m in messages:
        if m.has_key("media"):
            photos.append(m)
    print("Found", colored("%d" % len(photos), "red"), "Photos")
    print(colored("Downloading photos to [%s]" % outdir, "yellow"))
    sys.stdout.flush()
    donecount = 0
    for p in photos:
        command = b"load_photo %s" % (p['id'])
        res = json.loads(sendRecv(s, command), strict=False)
        shutil.move(res['result'], outdir)
        donecount += 1
        print(colored("\r%d done" % donecount, "green"),end='')
        sys.stdout.flush()
    print(colored("\n [Complete]", 'green'))
    sys.stdout.flush()
    code = 0
except:
    raise
finally:
    s.close()

sys.exit(code)
