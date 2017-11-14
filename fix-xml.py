from __future__ import with_statement
import re
import sys
import os
from contextlib import nested


def clean(filename):
	# delete any byte that's between 0x00 and 0x1F except 0x09 (tab), 0x0A (LF), and 0x0D (CR).
	ctrlregex = re.compile(r'[\x01-\x08|\x0B|\x0C|\x0E-\x1F]')

	new_filename = "{}.old".format(filename)
	os.rename(filename, new_filename)

	with open(filename, "wb") as destination:
		with open(new_filename, "rb") as source:

			for counter, line in enumerate(source, 1):
				rObj = re.search(ctrlregex, line)
				if rObj is not None:
					print(counter)
					newLine = re.sub(ctrlregex, '', line)
					destination.write(newLine)
				else:
					destination.write(line)

	os.remove(new_filename)


def usage():
	print("Usage: python fix-xml.py release directory, where release is for example 20091101")
	sys.exit()


def main(argv):
	if len(argv) == 0 or len(argv[0]) != 8:
		usage()
	try:
		int(argv[0])
	except ValueError:
		usage()
		sys.exit()

	if len(argv) > 1 and os.path.isdir(argv[1]):
		path = argv[1] + '/'
	else:
		path = ''

	release = argv[0]

	for data_type in ['labels', 'releases', 'masters', 'artists']:
		filename = os.path.join(path, 'discogs_{}_{}.xml'.format(release,
                                                                 data_type))
		clean(filename)


if __name__ == '__main__':
	main(sys.argv[1:])

