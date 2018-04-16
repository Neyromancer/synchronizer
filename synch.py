import argparse
from pathlib import Path
from filecmp import dircmp, cmp

def daemonize():
	print("daemonized")	

"""
	compare files
"""
def cmp_files(f1, f2):
	p1 = Path(str(f1)).stat()
	p2 = Path(str(f2)).stat()
	if p1.st_mtime == p2.st_mtime and \
		p1.st_size == p2.st_size:
		return True
	return False

"""
	in case of this program working
	as a daemon exclude updated files
	from checking for sometime as
	otherwise we can fall into infinite
	recursion OR find the way to copy
	file from srd dir to dst dir
	with exact parameters
"""
def update_dirs(f1, f2):
	p1 = Path(str(f1)).stat()
	p2 = Path(str(f2)).stat()
	if (p1.st_mtime > p2.st_mtime or \
		p1.st_size > p2.st_size) or \
		(p1.st_mtime > p2.st_mtime and \
		p1.st_size > p2.st_size):
		print("file %s is copied into %s" % (str(f1), str(Path(str(f2)).parents[0])))
	else:
		print("file %s is copied into %s" % (str(f2), str(Path(str(f1)).parents[0])))
	

def cmp_src_dst(crnt_dir, args):
	for i in args:
		if Path(i).exists():
			print(i)

def process_src_flg(args):
	crnt_dir = Path.cwd()
	if len(args) > 1:
		cmp_src_dst(crnt_dir, args)
	else:
		if Path(args[0]).exists() and Path(crnt_dir).exists():
			if Path(args[0]).is_dir():
				dcmp = dircmp(str(crnt_dir), args[0])
				for name in dcmp.left_only:
					print("file name is %s" % name)
			elif Path(args[0]).is_file():
				print("path %s is file" % (args[0]))
				for fname in Path(str(crnt_dir)).iterdir():
					if not cmp_files(args[0], fname):
						update_dirs(args[0], fname)
		

def parse_commands():
	parser = argparse.ArgumentParser(prog="synch", 
																	description="%(prog)s - remote (and local) object-synchronizer tool", 
																	usage="%(prog)s [OPTION] [SRC_PATH] [DEST_PATH]")
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
	parser.add_argument("--version", help="print version",
											action="version", version="%(prog)s v1.0")
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
	if args.src:
		process_src_flg(args.src)

def main():
	parse_commands()
	daemonize()

if __name__ == "__main__":
	main()
