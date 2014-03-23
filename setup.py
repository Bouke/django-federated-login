import sys

from distutils.core import setup
from setuptools import find_packages

install_requires = [
    'Django >=1.4.2, <1.7',
]

if sys.version_info > (3,):
    install_requires.append('python3-openid >=3.0.3, <3.1')
else:
    install_requires.append('python-openid == 2.2.5')

setup(
    name='django-federated-login',
    version='1.0.0',
    author='Bouke Haarsma',
    author_email='bouke@webatoom.nl',
    packages=find_packages(),
    url='http://github.com/Bouke/django-federated-login',
    description='Provides federated login (SSO) to Django projects',
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Security',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)
