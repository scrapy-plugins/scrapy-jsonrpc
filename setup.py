from os.path import dirname, join
from setuptools import setup, find_packages


setup(
    name='scrapy-jsonrpc',
    version='0.3.0',
    url='https://github.com/scrapy/scrapy-jsonrpc',
    description='Scrapy extenstion to control spiders using JSON-RPC',
    author='Scrapy developers',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'Twisted>=10.0.0',
        'Scrapy>=0.24.0',
        'six>=1.5.2',
    ],
)
