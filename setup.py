from setuptools import setup

def readme():
	with open("README.rst") as f:
		return f.read()
install_requires = [
	"requests",
	"beautifulsoup4",
	"rich"
]

setup(name="bsnlscripts",
	version="0.1",
	description="Collection of scripts for BSNL broadband connection.",
	long_description=readme(),
	classifiers=[
	"Development Status :: 3 - Alpha",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3.7",
	"Topic :: Utilities",
	],
	keywords="bsnl scripts",
	url="http://github.com/meashishsaini/bsnl",
	author="Ashish Saini",
	author_email="sainiashish08@gmail.com",
	license="MIT",
	packages=["bsnl"],
	install_requires=install_requires,
	# test_suite="nose.collector",
	# tests_require=["nose", "nose-cover3"],
	entry_points={
	"console_scripts": ["bsnl=bsnl.main:parse"],
	},
	include_package_data=True,
	zip_safe=False)
