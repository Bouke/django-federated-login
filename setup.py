from distutils.core import setup

setup(
    name='django-federated-login',
    version='0.1.3',
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
        'http://github.com/Bouke/python-openid/downloads',
    ],
    install_requires=[
        'python-openid == 2.2.5-bouke0',
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
