#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
#from subprocess import check_output
import subprocess
import datetime

var_log = "/var/log/syslog"

def get_last_log_msg():
  try:
    cmd = "tail -n1000 " + var_log
    log_msg = subprocess.check_output(cmd, shell=True)
    indx = str(log_msg).find(str("New USB"))
    if indx >= 0:
      str(log_msg)[indx:].find(
  except subprocess.CalledProcessError as er:
    return er.returncode
  #print(log_msg)

def dir_mounted():
  d = datetime.datetime.now().time()
  print("current hour is {}".format(str(d.hour)))
  print("current minute is {}".format(str(d.minute)))
  get_last_log_msg()

if __name__ == "__main__":
  dir_mounted()
