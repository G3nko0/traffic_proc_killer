
import math
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
import psutil
import argparse
import re


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
   

if __name__ == "__main__":
Z
	parser = argparse.ArgumentParser(description='Pass process name(s) and traffic limit.')
	parser.add_argument('processes', metavar='process_names', type=str, nargs='+',
	                    help='process(es) name(s), for e.g. "tmux"')
	parser.add_argument('--limit', dest='limit', default=1099511627776, type=float,
	                    help='limit of traffic when to stop processes in bytes! (default: 1 TB)')

	args = parser.parse_args()

	traffic = sum([ifdata.bytes_recv + ifdata.bytes_sent  for _,ifdata in psutil.net_io_counters(pernic=True).items()])

	print("Total traffic: ", convert_size(traffic))

	conv_limit = convert_size(args.limit)
	if traffic >= args.limit:
		print("Limit of {} reached".format(conv_limit))
		print("Looking process(es) {} to kill".format(args.processes))

		for proc in psutil.process_iter():
			for tproc in args.processes:
				match = re.search(r'\b{}\b'.format(tproc), proc.name())
				if match:
					print('Found {}.'.format(proc.name()), end = ' ')
					proc.kill()
					print('Killed')
		print('Done')
	else:
		print("Limit of {} not reached".format(conv_limit))