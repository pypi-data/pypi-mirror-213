from codecs import open
from os import path
from setuptools import setup, find_packages

basedir = path.abspath(path.dirname(__file__))
with open(path.join(basedir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read().replace('\r\n', '\n')

setup(
    name='sc-editor',
    version='0.93',
    description='냥코에디터 한글화',
    long_description='냥코에디터 한글화',
    long_description_content_type='text/markdown',
    author='cintagramabp',
    author_email='',
    url='',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    keywords='python, template',
    python_requires='>=3',
)