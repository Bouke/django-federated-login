from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-federated-login',
    version='0.3.0',
    author='Bouke Haarsma',
    author_email='bouke@webatoom.nl',
    packages=find_packages(),
    url='http://github.com/Bouke/django-federated-login',
    description='Provides federated logins to django projects',
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=[
        'python-openid == 2.2.5',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)
