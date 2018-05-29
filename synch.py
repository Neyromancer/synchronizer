import argparse, textwrap
from pathlib import Path
from filecmp import dircmp, cmp
from synch_server import *
PROG_VERSION = 1.00

def parse_commands():
	global PROG_VERSION
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

	localSync = LocalSync()
	if args.verbose:
		localSync.verbose = True
		localSync.quiet = False
	if args.quiet:
		localSync.quiet = True
		localSync.verbose = False

	if args.src:
		localSync.process_src_flg(args.src)
	elif args.dest:
		LocalSync.process_dest_flg(args.dest)
	elif args.synchcurrdir:
		LocalSync.process_src_flg(args.synchcurrdir)

def main():
	parse_commands()
	#daemonize()

if __name__ == "__main__":
	main()
