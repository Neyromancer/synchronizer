#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import logger
import inspect
import os.path
import os
import re
import string
import subprocess
import sys
import time

KERNEL_LOG = "/var/log/kern.log"
OUTPUT = os.path.abspath("/home/dmitry/workspace/git/"\
                         "usb_listener/output_file")

def is_valid(tmp_str):
  for el in tmp_str:
    if el.isalpha():
      return True
  return False

def is_valid_volume(tmp_disk):
  cnt_ltr = 0
  cnt_dgt = 0
  for el in tmp_disk:
    if el.isalpha():
      cnt_ltr = cnt_ltr + 1

    if el.isdigit():
      cnt_dgt = cnt_dgt + 1

  if cnt_ltr and cnt_dgt and \
     cnt_ltr < 2 and \
     (cnt_dgt >= cnt_ltr):
    return True
  return False

def parse_flog():
  tmp_str = ""
  with open(KERNEL_LOG, 'r') as f:
    tmp_str = f.readlines()

  indx = str(tmp_str).rfind("usb")
  tmp_str = str(tmp_str)[indx + 1:]
  print("index is {}".format(indx))
  while (indx != -1):
    indx = tmp_str.find('[')
    indx_end = tmp_str.find(']')
    if indx < 0 or indx_end < 0:
      break

    tmp = tmp_str[indx + 1:indx_end]
    print("tmp is {}".format(tmp))
    if is_valid(tmp):
      return tmp
    tmp_str = tmp_str[indx_end + 1:]
  return None    

"""
  delete non alphanumeric
  symbols from passed arg
"""
def dev_name_format(tmp_nm):
  res = tmp_nm
  for el in tmp_nm:
    if not el.isdigit() and not el.isalpha():
      res = res.replace(el, "")

  return res

"""
 T > G > M > K
 if ext1 > ext2 return 1
 if ext1 == ext2 return 0
 if ext1 < ext2 return -1
"""
def cmp_ext(ext1, ext2):
  if ext1 == ext2:
    return 0
  else:
    """ 
      ext2 anything else but T
      equality checked at the step above
    """
    if ext1 == 'T':
      return 1
    elif ext1 == 'G':
      if ext2 == 'T':
        return -1
      else: return 1
    elif ext1 == 'M':
      if ext2 == 'T' or \
         ext2 == 'G':
        return -1
      else: return 1
    else:
      return -1
"""
 if dev_dcit1 > dev_dict2 return 1
 if dev_dict1 == dev_dict2 return 0
 if dev_dict1 < dev_dict2 return -1
"""
def cmp_dev(dev_dict1, dev_dict2):
  for dev_nm1 in dev_dict1.keys():
    for dev_nm2 in dev_dict2.keys():
      dev_vol1 = dev_dict1[dev_nm1]
      dev_vol2 = dev_dict2[dev_nm2]
      if len(dev_vol1) > \
         len(dev_vol2):
        print("first")
        if not cmp_ext(dev_vol1[-1],dev_vol2[-1]) >= 0:
          return 1
        else: return -1
      elif len(dev_vol1) == \
           len(dev_vol2):
        print("2nd")
        return cmp_ext(dev_vol1[-1],dev_vol2[-1])      
      else:
        print("3d")
        if cmp_ext(dev_vol1[-1], dev_vol2[-1]) <= 0:
          return -1
        else: return 1

def biggest_volume_dev(dev_volumes):
  tmp_dict1 = dict()
  tmp_dict2 = dict()
  for dev_nm in dev_volumes.keys():
    if tmp_dict1:
      tmp_dict2[dev_nm] = dev_volumes[dev_nm]
      if cmp_dev(tmp_dict1, tmp_dict2) >= 0:
        return tmp_dict1
      else: return tmp_dict2
    if not tmp_dict1:
      tmp_dict1[dev_nm] = dev_volumes[dev_nm]

"""
  find actual usb device name
  call lsblk program and parse its output
  the dev name with the biggest volume
  is what we are looking for
"""
def find_actual_dev(tmp_dev):
  func = inspect.currentframe().f_back.f_code
  print("in {} ln is {} arg is {}".format(func.co_name,\
                                          func.co_firstlineno,\
                                          tmp_dev))
  try:
    ret = None
    if sys.version_info[0] < 3:
      print("python version is {0}.{1}".format(sys.version_info[0],\
                                          sys.version_info[1]))
      print("Use here appropriate call method")
    else:
      ret = subprocess.run(["lsblk"], \
                           stdout=subprocess.PIPE, \
                           stderr=subprocess.DEVNULL)
  except subprocess.CalledProcessError as er:
    print("exception output {} and err_code {}" \
          .format(er.returncode,er.output)) 
  if ret.stdout:
    print("in {} ln is {} arg is {}".format(func.co_name,\
                                            func.co_firstlineno,\
                                            tmp_dev))
    tmp_str = ret.stdout.decode("utf-8")
    indx = tmp_str.find(tmp_dev)
    if indx > 0:
      tmp_dev_res = tmp_str[indx:]
      tmp_dev_lns = tmp_dev_res.split("\n")
      dev_volumes = dict()
      for el in tmp_dev_lns:
        if tmp_dev in el and \
           "part" in el:
          tmp_elms = el.split()
          for i in tmp_elms:
            if tmp_dev in i:
              name = dev_name_format(i)
            if is_valid_volume(i):
              dev_volumes[name] = i
      if len(dev_volumes) > 1:
        dev_vol = biggest_volume_dev(dev_volumes)
        print("dev_volume is {}".format(dev_vol))
        return dev_vol
  return None

"""
  build path to the disk we want to mount
"""
def bld_dsc_path(tmp_dev):
  dsc_nm = find_actual_dev(tmp_dev)
  if dsc_nm:
    print("disc_nm is {}".format(dsc_nm))
    return ("/dev/" + dsc_nm)
  return dsc_nm

def get_dev():
  tmp_dev_nm = parse_flog()
  print("tmp dev name {}".format(tmp_dev_nm))
  if tmp_dev_nm:
    return bld_dsc_path(tmp_dev_nm)
  return None

def int_from_str(orig_str):
  is_frst = False
  is_dgt = False
  dgt = 0
  for i in orig_str:
    if i.isdigit() and not is_frst:
      dgt = dgt * 10 + int(i)
      is_dgt = True

    if is_dgt and not i.isdigit():
      is_frst = True

  return dgt

def check_flog():
  try:
    ret = None
    if sys.version_info[0] < 3:
      print("python version is {0}.{1}".format(sys.version_info[0],\
                                          sys.version_info[1]))
      print("Use here appropriate call method")
    else:
      ret = subprocess.run(["inotifywatch","-t5","-e",\
                           "modify", KERNEL_LOG], \
                           stdout=subprocess.PIPE, \
                           stderr=subprocess.DEVNULL)
  except subprocess.CalledProcessError as er:
    print("exception output {} and err_code {}" \
          .format(er.returncode,er.output))

  if ret.stdout:
    tmp = ret.stdout.decode("utf-8")
    print("output is {}".format(tmp))
    dgt = int_from_str(tmp)
    print("number of asking kern.log is {}".format(dgt))
    if dgt > 0:
      dev = get_dev()
      print("device is {}".format(dev))
      #return True
  #return False


"""
  mount usb_dev device to
  /media/current_user_name/mnt[number]
  and print result
"""
#def usb_mnt(usb_dev):
#  try:
#    ret = None
#    if sys.version_info[0] < 3:
#      print("python version is {0}.{1}".format(sys.version_info[0],\
#                                          sys.version_info[1]))
#      print("Use here appropriate call method")
#    else:
#      ret = subprocess.run(["mount", usb_dev], \
#                           stdout=subprocess.PIPE, \
#                           stderr=subprocess.DEVNULL)
#  except subprocess.CalledProcessError as er:
#    print("exception output {} and err_code {}" \
#          .format(er.returncode,er.output)) 

def daemonize():
  running=True
  cnt = 1
  while(running):
    if cnt > 10:
      running=False
    check_flog()
    cnt = cnt + 1

if __name__ == "__main__":
  check_flog()
  #daemonize()
