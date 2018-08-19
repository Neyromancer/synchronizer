#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import logger
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
  while (indx != -1):
    indx = tmp_str.find('[')
    indx_end = tmp_str.find(']')
    if indx < 0 or indx_end < 0:
      break

    tmp = tmp_str[indx + 1:indx_end]
    if is_valid(tmp):
      return tmp
      break
    tmp_str = tmp_str[indx_end + 1:]

  return None    

def dev_name_format(tmp_nm):
  res = tmp_nm
  for el in tmp_nm:
    if not el.isdigit() and not el.isalpha():
      res = res.replace(el, "")

  return res

"""
 T > G > M > K
"""
def cmp_ext(ext1, ext2)
  if 

def compare_dev(dev_dict1, dev_dict2):
  for dev_nm1 in dev_dict1.keys():
      for dev_nm2 in dev_dict2.keys():
        if len(dev_dict1[dev_nm1]) > \
          len(dev_dict2[dev_nm2]):
          print("first")
          print(dev_dict1[dev_nm1])
        elif len(dev_dict1[dev_nm1]) == \
             len(dev_dict2[dev_nm2]):
          
          print("length is {}".format(len(dev_dict2[dev_nm2])))
        else:
          print("2nd")
          print(dev_dict2[dev_nm2])

def dev_biggest_volume_dev(dev_volumes):
  tmp_dict1 = dict()
  tmp_dict2 = dict()
  for dev_nm in dev_volumes.keys():
    if tmp_dict1:
      tmp_dict2[dev_nm] = dev_volumes[dev_nm]
      compare_dev(tmp_dict1, tmp_dict2)
    if not tmp_dict1:
      tmp_dict1[dev_nm] = dev_volumes[dev_nm]

"""
  find actual usb device name
  call lsblk program and parse its output
  the dev name with the biggest volume
  is what we are looking for
"""
def find_actual_dev(tmp_dev):
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
        dev_biggest_volume_dev(dev_volumes)

"""
  build path to the disk we want to mount
"""
def dsc_path(tmp_dev):
  find_actual_dev(tmp_dev)


def get_dev():
  tmp_dev_nm = parse_flog()
  print(tmp_dev_nm)
  if tmp_dev_nm:
    dev = dsc_path(tmp_dev_nm)
    return dev
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
    dgt = int_from_str(tmp)
    if dgt > 0:
      dev = get_dev()
      print(dev)
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
