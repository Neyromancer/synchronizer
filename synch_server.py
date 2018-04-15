from pathlib import Path

def cmp_src_dst(args):
	for i in args:
		print(i)

def process_src_flag(args):
	if len(args) > 1:
		cmp_src_dst(args)
	else:
		print("current dir %s" % str(Path.cwd()))
