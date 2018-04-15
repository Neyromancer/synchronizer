import argparse
from pathlib import Path
from filecmp import dircmp

def daemonize():
	print("daemonized")	

def cmp_src_dst(args):
	for i in args:
		print(i)

def process_src_flg(args):
	if len(args) > 1:
		cmp_src_dst(args)
	else:
		crnt_dir = Path.cwd()
		dcmp = dircmp(crnt_dir, args)
		print ("files in %s are" % str(crnt_dir))
		print("files in current dir is %s" % dcmp.left_only)
		#for f in dcmp.left_list:
			#print(f)
		

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
	process_src_flg(args.src)

def main():
	parse_commands()
	daemonize()

if __name__ == "__main__":
	main()
