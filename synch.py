import argparse, textwrap
from pathlib import Path
from filecmp import dircmp, cmp
PROG_VERSION = 1.00
VERBOSE = False
QUIET = False

"""
class VersionAction(argparse.Action):
	def __init__(self, option_strings, dest, nargs=None, **kwargs):
#		if nargs is not None:
#			raise ValueError("nargs not allowed")
		super(VersionAction, self).__init__(option_strings, dest, **kwargs)
	def __call__(self, parser, namespace, version, option_string=None):
		print("parser is %s" % parser)
		print("namespace is %s" % namespace)
		#print("values is %s " % values)
		setattr(namespace, version, self.dest)
"""

def daemonize():
	print("daemonized")	

"""
	compare files
"""
def is_eql_objs(f1, f2):
	global VERBOSE
	file_name1 = Path(f1).name
	file_name2 = Path(f2).name
	if file_name1 != file_name2:
		return False

	stat_p1 = Path(str(f1)).stat()
	stat_p2 = Path(str(f2)).stat()
	if stat_p1.st_mtime == stat_p2.st_mtime and \
		stat_p1.st_size == stat_p2.st_size:
		if VERBOSE:
			print("file system objects: \n{} and \n{} are equal".format(file_name1, file_name2))
		return True

		if VERBOSE:
			print("file system objects: \n{} and \n{} are not equal".format(file_name1, file_name2))
	return False


def find(src_obj, dst_dir):
	for name in dst_dir.iterdir():
		if src_obj == name:
			return True
	return False

"""
	in case of this program is working
	as a daemon exclude updated files
	from checking for sometimes as
	otherwise we can fall into infinite
	recursion OR find the way to copy
	file from src dir to dst dir
	with exact parameters
"""
#PosixPath dst_pth
#PosizPath src_pth
def update_files(dst_pth, src_pth):
	st_dst = Path(str(dst_pth)).stat()
	st_src = Path(str(src_pth)).stat()
	if (st_dst.st_mtime > st_src.st_mtime or \
		st_dst.st_size > st_src.st_size) or \
		(st_dst.st_mtime > st_src.st_mtime and \
		st_dst.st_size > st_src.st_size):
			if not QUIET:
				print("file {} is copied into {}".format(Path(dst_pth).name, Path(str(src_pth)).parent))
	else:
		if not QUIET:
			print("file {} is copied into {}".format(Path(src_pth).name, Path(str(dst_pth)).parent))


#PosixPath dst_pth
#PosizPath src_pth
def cpy_dirs(dst_pth, src_pth):
	dst_pth.mkdir(exist_ok=False)
	if VERBOSE:
		print("directory {} was created in destination path {}".format(dst_pth.name, dst_pth.parent))
	process_path(str(dst_pth),str(src_pth))

#PosixPath dst_pth
#PosizPath src_pth
def cpy_files(dst_pth, src_pth):
	dst_pth.touch(exist_ok=False)
	wrt_str = Path(src_pth).read_bytes()
	dst_pth.write_bytes(wrt_str)
	if VERBOSE:
		print("datum from file {} were copied into file {}".format(src_pth, dst_pth))


#string dst
#string src
def cpy_objs(dst, src):
	dst_pth = Path(dst).joinpath(Path(src).name)
	if Path(src).is_dir():
		cpy_dirs(dst_pth, src)
	elif Path(src).is_file():
		cpy_files(dst_pth, src)

def process_pth_list(args):
	for i in range(1, len(args)):
		process_path(args[i], args[0])

"""
	def process_objs(string: dst_pth, string src_pth, list: pth_list, bool: is_cpy)
"""
def process_objs(dst_pth, src_pth, pth_list, is_cpy):
	for name in pth_list:
		full_src_pth = Path(src_pth).joinpath(name)
		if is_cpy:
			cpy_objs(dst_pth, full_src_pth)
		else:
			full_dst_pth = Path(dst_pth).joinpath(name)
			process_path(str(full_dst_pth), str(full_src_pth))

#string dst_pth
#string src_pth
def process_path(dst_pth, src_pth):
	if Path(src_pth).exists() and Path(dst_pth).exists():
			if Path(src_pth).is_dir():
				dcmp = dircmp(dst_pth, src_pth)
				is_cpy = True
				if len(dcmp.right_only):
					process_objs(dst_pth, src_pth, dcmp.right_only, is_cpy)
				if len(dcmp.left_only):
					process_objs(dst_pth, src_pth, dcmp.left_only, is_cpy)
				if len(dcmp.common):
					is_cpy = False
					process_objs(dst_pth, src_pth, dcmp.common, is_cpy)
			elif Path(src_pth).is_file():
				if Path(dst_pth).is_dir():
					if not find(src_pth, dst_pth):
						cpy_objs(dst_pth, src_pth)
					else:
						for fname in Path(dst_pth).iterdir():
							if not is_eql_objs(src_pth, fname):
								update_files(src_pth, fname)
				else:
					if not is_eql_objs(src_pth, dst_pth):
						update_files(src_pth, dst_pth)
					else:
						print("Nothing to synchronize. Everything is already synchronized")


"""
	function defines case with src path fed.
	src path compared with current dir
	def process_src_flg(list: args)
"""
def process_src_flg(args):
	if len(args) > 1:
		process_pth_list(args)
	else:
		crnt_dir = Path.cwd()
		process_path(str(crnt_dir), args[0])	

#def process_dest_flg(list: args)
def process_dest_flg(args):
	crnt_dir = Path.cwd()
	args.insert(0,str(crnt_dir))
	process_pth_list(args)

def parse_commands():
	global PROG_VERSION
	global VERBOSE
	global QUIET
	str_v = "v{:0.2f} \nThis is free software: you are free to change and redistribute it. \nThere is NO WARRANTY, to the extent permitted by law. \n\nWritten by Dmitry Kormulev.".format(PROG_VERSION)

	parser = argparse.ArgumentParser(prog="synch", 
																	description="%(prog)s - remote (and local) object-synchronizer tool", 
																	usage="%(prog)s [OPTION] [SRC_PATH] [DEST_PATH]",
																	formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("synchcurrdir", nargs='*')
	parser.add_argument("-v", "--verbose", help="increase verbosity", 
											action="store_true")
	parser.add_argument("-q", "--quiet", help="suppress non-error messages", 
											action="store_true")
	parser.add_argument("--delete", help="delete extraneuos files from dest and src dirs", 
											action="store_true")
	parser.add_argument("-f", "--force", help="force any current action",
											action="store_true")

	parser.add_argument("--no-recursive", help="turn off dir's recursive parsing",
											action="store_true")

	parser.add_argument("--version", help="output version information and exit", action="version", version="%(prog)s " + str_v)

	parser.add_argument("-d", "--dest", help="set destination dirs/files",
											nargs='*')
	parser.add_argument("-s", "--src", help="set source dirs/files",
											nargs='*')
	parser.add_argument("-e", "--exclude", help="exclude dirs/files from synchronization",
											nargs='*', metavar="PATH")
	parser.add_argument("--progress", help="print synchronization progress",
											action="store_true")
	parser.add_argument("-l", "--links", help="copy symlinks as symlinks",
											action="store_true")
	parser.add_argument("-L", "--transform-links", help="transform symlinks into referent files/dirs",
											action="store_true")
	parser.add_argument("-H", "--hard-links", help="preserve hard links",
											action="store_true")
	parser.add_argument("-P", "--perms", help="preserve permissions",
											action="store_true")
	parser.add_argument("-G", "--group", help="preserve group",
											action="store_true")
	parser.add_argument("-b", "--backup", help="make backups of synchronized objects",
											action="store_true")
	parser.add_argument("-T", "--times", help="preserve modification times",
											action="store_true")
	parser.add_argument("-u", "--default-dirs", help="add default dirs", nargs='*')
	parser.add_argument("-r", "--remove-dirs", help="remove default dirs", nargs='*', metavar="DEFAULT_DIRS")
	parser.add_argument("-c", "--config-include", help="add provided path with set options to configuration file", nargs='*', metavar="COMMAND")
	args = parser.parse_args()
	if args.verbose:
		VERBOSE = True
		QUIET = False
	elif args.quiet:
		QUIET = True
		VERBOSE = False

	if args.src:
		process_src_flg(args.src)
	elif args.dest:
		process_dest_flg(args.dest)
	elif args.synchcurrdir:
		process_src_flg(args.synchcurrdir)

def main():
	parse_commands()
	daemonize()

if __name__ == "__main__":
	main()
