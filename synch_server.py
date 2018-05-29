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
        dcmp = dircmp(dst_pth, src_pth)
        is_cpy = True
        if len(dcmp.right_only):
          self.process_objs(dst_pth, src_pth, dcmp.right_only, is_cpy)
        
        if len(dcmp.left_only):
          self.process_objs(dst_pth, src_pth, dcmp.left_only, is_cpy)

        if len(dcmp.common):
          is_cpy = False
          self.process_objs(dst_pth, src_pth, dcmp.common, is_cpy)
      elif Path(src_pth).is_file():
        if Path(dst_pth).is_dir():
          if not self.find(Path(src_pth), Path(dst_pth)):
            self.cpy_objs(dst_pth, src_pth)
          else:
            for fname in Path(dst_pth).iterdir():
              if not self.is_eql_objs(src_pth, fname):
                self.update_files(src_pth, fname)
        else:
          if not self.is_eql_objs(src_pth, dst_pth):
            self.update_files(src_pth, dst_pth)
          else:
            if not self.quiet:
              print("Nothing to synchronize. Everyting is already synchronized")
      elif Path(src_pth).is_dir() and Path(dst_pth).is_file():
        self.process_pth(src_pth, dst_pth)

  """
    def process_objs(string: dst_pth, string: src_pth, list: pth_lst, book: is_cpy)
  """
  def process_objs(dst_pth, src_pth, pth_lst, is_cpy):
    for name in pth_lst:
      full_src_pth = Path(src_pth).joinpath(name)
      if is_cpy:
        self.cpy_objs(dst_pth, full_src_pth)
      else:
        full_dst_pth = Path(dst_pth).joinpath(name)
        self.process_pth(str(full_dst_pth), str(full_src_pth))
    
  def process_pth_lst(args):
    for i in range(1, len(args)):
      self.process_pth(args[i], args[0])

  #string dst
  #string src
  def cpy_objs(dst, src):
    dst_pth = Path(dst).joinpath(Path(src).name)
    if Path(src).is_dir():
      self.cpy_dirs(dst_pth, src)
    elif Path(src).is_file():
      self.cpy_files(dst_pth, src)

  #PosixPath dst_pth
  #PosixPath src_pth
  def cpy_files(dst_pth, src_pth):
    if not dst_pth.exists():
      dst_pth.touch(exist_ok=False)
    wrt_str = Path(src_pth).read_bytes()
    dst_pth.write_bytes(wrt_str)

    from os import utime, stat
    stat_src = stat(str(src_pth))
    utime(str(dst_pth), times=(stat_src.st_atime, stat_src.st_mtime))
    if self.verbose:
      print("datum from file {} were copied into file {}".format(src_pth, dst_pth))

  #PosixPath dst_pth
  #PosixPath src_pth
  def cpy_dirs(dst_pth, src_pth):
    dst_pth.mkdir(exist_ok=False)
    if self.verbose:
      print("directory {} was created in destination path {}".format(dst_pth.name, dst_pth.parent))
    self.process_pth(str(dst_pth), str(src_pth))

  #PosixPath dst_pth
  #PosixPath src_pth
  def update_files(dst_pth, src_pth):
    st_dst = Path(str(dst_pth)).stat()
    st_src = Path(str(src_pth)).stat()
    if (st_dst.st_mtime > st_src.st_mtime or \
      st_dst.st_size > st_src.st_size) or \
      (st_dst.st_mtime > st_src.st_mtime and \
      st_dst.st_size > st_src.st_size):
        if not self.quiet:
          print("file {} is copied into {}".format(Path(dst_pth).name, Path(str(src_pth)).parent))
          self.cpy_files(Path(src_pth), Path(dst_pth))
    else:
      if not self.quiet:
        print("file {} is copied into {}".format(Path(src_pth).name, Path(str(dst_pth)).parent))
        self.cpy_files(Path(dst_pth), Path(src_pth))

  #PosixPath: src_obj
  #PosixPath: dst_dir
  def find(src_obj, dst_dir):
    for fanem in dst_dir.iterdir():
      if src_obj.name == fname.name:
        return True
    return False

  """
    compare files
    string: f1
    string: f2
  """  
  def is_eql_objs(f1, f2):
    file_name1 = Path(f1).name
    file_name2 = Path(f2).name
    if file_name1 != file_name2:
      return False

    stat_p1 = Path(f1).stat()
    stat_p2 = Path(f2).stat()
    if stat_p1.st_mtime == stat_p2.st_mtime and \
      stat_p1.st_size == stat_p2.st_size:
      if self.verbose:
        print("file system objects: \n{} and \n{} \nare equal".format(f1, f2))
      return True

      if self.verbose:
        print("file system objects: \n{} and \n{} are not equal".format(f1, f2))
      return False
