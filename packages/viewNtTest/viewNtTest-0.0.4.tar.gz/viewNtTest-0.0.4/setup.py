from setuptools import setup, find_packages
import os
import menu

setup(name = 'viewNtTest',
version = menu.__version__,
author = 'Scyther',
author_email = 'leroy_mathieu@live.fr',
keywords = 'test packages views',
classifiers = ['Topic :: Education'],
url='https://github.com/NewtonExpertise/test_pip.git',
packages = find_packages("menu"),
description = 'test_ajout_pip',
long_description = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
license = 'GPL V3',
plateformes = 'ALL',
include_package_data=True,
)