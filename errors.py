import traceback
import syslog

errs = {
  'succ'        : ("'SUCCESS'", 0),
  'error'       : ("'ERROR: %s'", 1),
  'warn'        : ("'WARNING: %s'", 2),
  'fail'        : ("'FAIL: %s'". 3),
}

class errClass(object):
  def __init__(self, name):
    self.noerrs = True
    self.nam = name
    syslog.openlog(self.name, syslog.LOG_PID, syslog.LOG_LOCAL2)
    
  def errorOut(self, err, mod=()):
    """
      method designed for logging errors and events
      INPUT:
        - err - structure consisting of error message and its code
        - mod - structure contains information additional to error message
      OUTPUT: -
    """ 
    msg = err[0] % mod
    exit_code = err[1]
    res = ""
    if exit_code == 0:
      res = "success"
    else:
      res = "failed"
      self.noerrs = False
    print(msg)
    syslog.syslog(syslog.LOG_ERR, "name={} message={} res={}".format(
        self.name, msg, res))
