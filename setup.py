from distutils.core import setup

setup(
    name='django-federated-login',
    version='0.1.2',
    author='Bouke Haarsma',
    author_email='bouke@webatoom.nl',
    packages=[
        'federated_login',
        'federated_login.auth'
    ],
    url='http://github.com/Bouke/django-federated-login',
    description='Provides federated logins to django projects',
    license='MIT',
    long_description=open('README.rst').read(),
    dependency_links=[
        'http://github.com/adieu/python-openid/tarball/03773fb96dff352bbda12538'
        '726dc5c46fe0316c#egg=python-openid',],
    install_requires=[
        'python-openid == 2.2.5',
        'Django >= 1.3.0',
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
