import os 
import sys 

#Make sure python 3
if not (sys.version_info[0] == 3):
    sys.exit("CeritQ currently supports Python 3.X only.")

try:
	from setuptools import setup 
except: 
	from disutils.core import setup 

#write verion to file so installation is not required to 
#import library prior to installation 
MAJOR = 0
MINOR = 1 
MICRO = 0 
VERSION = '{0}.{0}.{1}'.format(MAJOR,MINOR,MICRO)
NAME = 'Giallar'
URL = ''
AUTHOR = ''''''
AUTHOR_EMAIL = ''
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL

KEYWORDS = ['quantum','compiler','verification']

DESCRIPTION = 'A quantum compilation verification framework'

			  
REQUIRES = [
			'z3-solver>=4.8.9.0',
                      'astroid>=2.4.1',
                        'networkx',
                        'qutip',
                        'qiskit'
			]

INSTALL_REQUIRES = [
			'z3-solver>=4.8.9.0',
                        'astroid>=2.4.1',
                        'networkx',
                        'qutip',
                        'qiskit'
			]

PACKAGES = [
		'giallar',
        'giallar/preprocessor',
    	'verified_passes',
		'giallar/core',
		'giallar/core/spec',
		'giallar/core/impl',
        'giallar/qiskit_wrapper',
		'giallar/utility_library'
		]

#project needs a license 
LICENSE = ''

PLATFORMS=['linux', 'Mac OS']

CLASSIFIERS = [
	'Development Status :: Beta',
	'Intended Audience :: Science/Research',
	'Natural Language :: English',
    'Operating System :: Linux',
    'Programming Language :: Python :: 3.7.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Scientific/Engineering :: Verification',
]
version_file = 'version.txt'

def write_version(version_file=version_file):
	#open and overwrite old version file
    with open(version_file,'w+') as v:
	
        v.write("""version = {0}""".format(VERSION))

write_version()


try: 
	readme = open('README.md','r')
	LONG_DESCRIPTION= readme.read()
except:
	LONG_DESCRIPTION = ''

#perform setup
setup(
	name=NAME,
	version=VERSION,
	url=URL,
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	maintainer=MAINTAINER,
	maintainer_email = MAINTAINER_EMAIL,
	packages=PACKAGES,
	keywords=KEYWORDS,
	description=DESCRIPTION,
	platforms=PLATFORMS,
	install_requires=INSTALL_REQUIRES,
	classifiers=CLASSIFIERS
	)
