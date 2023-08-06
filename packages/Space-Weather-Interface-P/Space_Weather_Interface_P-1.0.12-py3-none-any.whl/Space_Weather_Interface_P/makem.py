# we need to make some god damn directories so python doesn't flip out
import os

def makem():
	#lets make sure the dirs exist
	dir1 = './images/'

	if os.path.exists(dir1):
		pass
	else:
		# Create the new directory
		os.mkdir(dir1)

	dir2 = './images/sdo'
	dir3 = './images/soho'

	# Check if the directory already exists
	if os.path.exists(dir2):
		pass
	else:
		# Create the new directory
		os.mkdir(dir2)
			
	if os.path.exists(dir3):
		pass
	else:
		# Create the new directory
		os.mkdir(dir3)
makem()