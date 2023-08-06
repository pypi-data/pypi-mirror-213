"""officetools setup"""
from os import path
import setuptools

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

import re
VERSIONFILE="officetools/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    author="Yves R. Sagaert",
    author_email="yves.r.sagaert@gmail.com",
    name='officetools',
    license="GNU GPLv3",
    description='Forecasting package for office automation',
    version=verstr,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yForecasting/officetools',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.5",
    # Enable install requires when publishing on the normal PyPi
    install_requires=[
        'pandas',
        'matplotlib',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
