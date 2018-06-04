#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from pathlib import Path
from error_handler import errClass

class LocalSync(object):
  """
  class which implements local synchronization
  """
  def __init__(self, **kwargs):
    self.verbose = False
    self.quiet = False
    self.delete = False
    self.force = False
    self.no_recursive = False
    self.progress = False
    self.links = False
    self.transform_links = False
    self.hard_links = False
    self.perms = False
    self.group = False
    self.backup = False
    self.times = False
    self.err = errClass("SYNCHRONIZER", "synchronizer")

  def set_verbose():
    self.verbose = True
    self.quiet = False

  def set_quiet():
    self.quiet = True
    self.verbose = False

  def is_verbose():
    return self.verbose

  def is_quiet():
    return self.quiet

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
    self.err.logOut("info", "Processing paths {} and {}".format(dst_pth, src_pth))
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
            if not self.is_quiet():
              self.err.logOut("info", "Nothing to synchronize. Everyting is already synchronized")
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
    if self.is_verbose():
      self.err.logOut("info", "Datum from file {} were copied into file {}".format(src_pth, dst_pth))
      print("Datum from file {} were copied into file {}".format(src_pth, dst_pth))

  #PosixPath dst_pth
  #PosixPath src_pth
  def cpy_dirs(dst_pth, src_pth):
    dst_pth.mkdir(exist_ok=False)
    if self.is_verbose():
      self.err.logOut("info","Directory {} was created in destination path {}".format(dst_pth.name, dst_pth.parent))
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
        if not self.is_quiet():
          self.err.logOut("info","file {} is copied into {}".format(Path(dst_pth).name, Path(str(src_pth)).parent))
          print("file {} is copied into {}".format(Path(dst_pth).name, Path(str(src_pth)).parent))
          self.cpy_files(Path(src_pth), Path(dst_pth))
    else:
      if not self.is_quiet():
        self.err.logOut("info","File {} is copied into {}".format(Path(src_pth).name, Path(str(dst_pth)).parent))
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
      if self.is_verbose:
        self.err.logOut("info","File system objects: \n{} and \n{} \nare equal".format(f1, f2))
        print("file system objects: \n{} and \n{} \nare equal".format(f1, f2))
      return True

      if self.is_verbose():
        self.err.logOut("info","File system objects: \n{} and \n{} are not equal".format(f1, f2))
        print("file system objects: \n{} and \n{} are not equal".format(f1, f2))
      return False
