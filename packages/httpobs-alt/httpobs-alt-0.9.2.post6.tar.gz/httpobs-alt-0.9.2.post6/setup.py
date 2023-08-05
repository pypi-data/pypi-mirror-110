#!/usr/bin/env python3

import os

from httpobs import SOURCE_URL, VERSION
from setuptools import setup, find_packages


__dirname = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(__dirname, 'README.md')) as readme:
    README = readme.read()

setup(
    name='httpobs-alt',
    version=VERSION,
    description='HTTP Observatory: a set of tests and tools to scan your website for basic web hygeine.',
    url=SOURCE_URL,
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
    ],
    author='April King',
    author_email='april@mozilla.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'amqp==2.3.2',
        'anyjson==0.3.3',
        'beautifulsoup4==4.6.3',
        'billiard==3.5.0.4',
        'celery==4.2.1',
        'certifi==2021.5.30',
        'chardet==3.0.4',
        'Click==7.0',
        'coverage==4.5.2',
        'flake8==3.6.0',
        'Flask==1.0.2',
        'httpobs-cli==1.0.2',
        'idna==2.7',
        'itsdangerous==1.1.0',
        'Jinja2==3.0.1',
        'kombu==4.2.1',
        'MarkupSafe==2.0.1',
        'mccabe==0.6.1',
        'nose==1.3.7',
        'pep8==1.7.1',
        'psutil==5.4.8',
        'psycopg2-binary==2.9.1',
        'publicsuffixlist==0.6.2',
        'pycodestyle==2.4.0',
        'pyflakes==2.0.0',
        'pytz==2018.7',
        'redis==2.10.6',
        'requests==2.20.1',
        'urllib3==1.24.3',
        'uWSGI==2.0.17.1',
        'vine==1.1.4',
        'Werkzeug==0.14.1',
    ],
    scripts=['httpobs/scripts/httpobs-local-scan',
             'httpobs/scripts/httpobs-mass-scan',
             'httpobs/scripts/httpobs-scan-worker'],
    zip_safe=False,
)
