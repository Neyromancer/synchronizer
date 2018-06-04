# -*- coding: utf-8 -*-

MESSAGE = {
  "succ"    : ("'SUCCESS', 0"),
  "error"   : ("'ERROR:'", 1),
  "warn"    : ("'WARNING:'", 2),
  "fail"    : ("'FAIL:'", 3)
}

def get_all_messages():
  return MESSAGE

def get_message(key):
  try:
    return MESSAGE[key]
  except KeyError:
    return None
