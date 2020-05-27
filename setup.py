from os import path

from setuptools import setup, find_packages

import jsonobj


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='jsonobj',
    version=jsonobj.__version__,
    py_modules=['jsonobj'],
    python_requires='>=2.7, !=3.0.*',

    description=jsonobj.__doc__,
    url='https://github.com/skitschy/pyJSONobj',
    author=jsonobj.__author__,
    author_email='s1kitschy@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='json',
    project_urls={
        'Documentation': 'https://pyjsonobj.readthedocs.io/',
        'Source': 'https://github.com/skitschy/pyJSONobj',
    }
)
