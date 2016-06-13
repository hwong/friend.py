from distutils.core import setup
import py2exe

setup(
	console=['friend.py'],
	options={
		"py2exe": {
			"bundle_files": 2
		}
	},
	zipfile=None
)