#!/usr/bin/env python

import os
import sys
import datetime
import time
import socket

host = os.getenv(
            "NERF_LISTEN_ON_HOST",
            "127.0.0.1").strip().lstrip()
port = int(os.getenv(
            "NERF_LISTEN_ON_PORT",
            "9000").strip().lstrip())
backlog = int(os.getenv(
            "NERF_LISTEN_BACKLOG",
            "5").strip().lstrip())
size = int(os.getenv(
            "NERF_LISTEN_SIZE",
            "1024").strip().lstrip())
sleep_in_seconds = float(os.getenv(
            "NERF_LISTEN_SLEEP",
            "0.5").strip().lstrip())
shutdown_hook = os.getenv(
            "NERF_LISTEN_SHUTDOWN_HOOK",
            "/tmp/shutdown-listen-server-{}-{}".format(host,
                                                       port)).strip().lstrip()

if os.path.exists(shutdown_hook):
    print(("Please remove the shutdown hook file: "
           "\nrm -f {}")
          .format(shutdown_hook))
    sys.exit(1)

now = datetime.datetime.now().isoformat()
print(("{} - Starting Server address={}:{} "
       "backlog={} size={} sleep={} shutdown={}")
      .format(now,
              host,
              port,
              backlog,
              size,
              sleep_in_seconds,
              shutdown_hook))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

msg = 0
while 1:
    client, address = s.accept()
    data = client.recv(size)
    if data:
        now = datetime.datetime.now().isoformat()
        print(("{} received msg={} "
               "data={} replying")
              .format(now,
                      msg,
                      data))
        msg += 1
        if msg > 1000000:
            msg = 0

        client.send(data)
    else:
        time.sleep(sleep_in_seconds)

    if os.path.exists(shutdown_hook):
        now = datetime.datetime.now().isoformat()
        print(("{} detected shutdown "
               "file={}")
              .format(now,
                      shutdown_hook))

    client.close()
# end of loop
