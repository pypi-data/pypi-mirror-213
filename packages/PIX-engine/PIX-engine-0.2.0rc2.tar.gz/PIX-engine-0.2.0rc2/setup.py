import io
import os

from setuptools import setup

# Package meta-data.
NAME = 'PIX-engine'
DESCRIPTION = 'Terminal game engine that is community supported and open source'
URL = 'https://github.com/Retaki/PIX'
VERSION = '0.2.0-RC2'
EMAIL = 'boxeigit@gmail.com'
AUTHOR = 'Retaki'
REQUIRES_PYTHON = '>=3.7.0'
REQUIRED = [
    'pyfiglet',
]
EXTRAS = {
    # 'fancy feature': ['django'],
}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    # packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    py_modules=['pix'],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)