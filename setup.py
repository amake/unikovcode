from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='unikovcode',
    version='1.0',
    description='A bot to tweet fake Unicode codepoints',
    long_description=long_description,
    url='https://github.com/amake/unikovcode',
    author='Aaron Madlon-Kay',
    author_email='aaron@madlon-kay.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='unicode markov twitter bot',
    py_modules=['unikovcode', 'bot'],
    install_requires=['tweepy']
)
