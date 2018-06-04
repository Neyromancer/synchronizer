#!/usr/bin/evn python
# -*- coding: utf-8 -*-
import traceback
import syslog
from message import get_message
import importlib

class errClass(object):
  def __init__(self, sype_name, name):
    self.noerrs = True
    self.sype_name = sype_name
    self.name = name
    importlib.reload(syslog)

  def logOut(self, msg, mod=()):
    try:
      syslog.openlog(self.name, syslog.LOG_PID, syslog.LOG_LOCAL2)
      """
        method designed for logging errors and events
        INPUT:
          - msg - structure consisting of loh message and its code
          - mod - structure contains information additional to error message
        OUTPUT: -
      """ 
      sys_msg = get_message(msg)
      if sys_msg:
        msg = msg[0] % mod
        exit_code = msg[1]
        res = ""
        if not exit_code:
          log_arg = syslog.LOG_INFO
          res = "success"
          self.noerrs = True
        else:
          if exit_code == 1:
            log_arg = syslog.LOG_ERR
          elif exit_code == 2:
            log_arg = syslog.LOG_WARNING
          elif exit_code == 3:
            log_arg = LOG_CRIT
          res = "failed"
          self.noerrs = False

        print(sys_msg)
        syslog.syslog(log_arg, "sype={} name={} message={} res={}".format(
                      self.sype_name, self.name, sys_msg, res))
        syslog.closelog()
      else:
        pass
    except KeyError:
      log(syslog.LOG_CRIT, "Key ERROR IN SYSLOG")
    except IndexError:
      log(syslog.LOG_CRIT, "Index ERROR IN SYSLOG")
