#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from pathlib import Path

class LocalSync(object):
  """
  class which implements local synchronization
  """
	def __init__(self, **kwargs):
    self.verbose = kwargs.get("verbose")
    self.quiet = kwargs.get("quiet")
    self.delete = kwargs.get("delete")
    self.force = kwargs.get("force")
    self.no_recursive = kwargs.get("no_recursive")
    self.progress = kwargs.get("progress")
    self.links = kwargs.get("links")
    self.transform_links = kwargs.get("transform_links")
    self.hard_links = kwargs.get("hard_links")
    self.perms = kwargs.get("perms")
    self.group = kwargs.get("group")
    self.backup = kwargs.get("backup")
    self.times = kwargs.get("times")

  # def process_dest_flg(self, list: args)
  def process_dest_flg(self, args):
    # reimplement Path functions with functions from os.*
    args.insert(0, str(Path.cwd()))
    self.process_pth_lst(args)

  """
    function defines case with src path fed.
    src path compared with current dir
    def process_src_flg(self, list: args)
  """
  def process_src_flg(self, args):
    if len(args) > 1:
      self.process_pth_lst(args)
    else:
      # reimplement Path functions with functions from os.*
      self.process_pth(str(Path.cwd()), args[0])

  #string dst_pth
  #string src_pth
  def process_pth(self, dst_pth, src_pth):
    # reimplement Path functions with functions from os.*
    if Path(src_pth).exist() and Path(dst_pth).exists():
      if Path(src_pth).is_dir() and Path(dst_pth).is_dir():
