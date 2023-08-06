from setuptools import setup, find_packages
import os


version = '1.0.0'

tests_require = [
    'Plone',
    'plone.app.testing',
    'responses',
]

install_requires = [
    'setuptools',
    'requests',
    'python-cas==1.6.0',
    'lxml',
    'six',
]

setup(
    name='wcs.adminauth',
    version=version,
    description='Administrative login for Plone sites using CAS.',
    long_description=(open('README.rst').read() + '\n' +
                      open(os.path.join('docs', 'HISTORY.txt')).read()),
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 6.0',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='',
    author='webcloud7 ag',
    author_email='mailto:m.leimgruber@webcloud7.ch',
    url='https://github.com/webcloud7/wcs.adminauth',
    license='GPL2',

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['wcs'],
    include_package_data=True,
    zip_safe=False,

    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    [plone.autoinclude.plugin]
    target = plone
    """,
)
