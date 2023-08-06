from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    with codecs.open(os.path.join(here, "CHANGELOG.md"), encoding="utf-8") as changelog:
        LONG_DESCRIPTION = readme.read() + '\n\n\n' + changelog.read()


VERSION = '0.0.1'
DESCRIPTION = 'Dot-Onion Services Manager Client'
KEYWORDS = ['tor', 'hosting', 'onion', 'hidden', 'services', 'server']


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License', 
    'Operating System :: Unix',
    'Programming Language :: Python :: 3',
]

setup(
    name="onion-server",
    version=VERSION,
    author="Erasmus A. Junior",
    author_email="eirasmx@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    licence='MIT',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['colorama'],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    py_modules=['onion_server'],
    entry_points = {'console_scripts':['onion = onion_server:main']},
)
