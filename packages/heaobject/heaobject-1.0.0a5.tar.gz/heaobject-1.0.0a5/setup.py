"""
Documentation for setup.py files is at http://setuptools.readthedocs.io/en/latest/setuptools.html
"""

import setuptools

setuptools.setup(name='heaobject',
                 version='1.0.0a5',
                 description='Data and other classes that are passed into and out of HEA REST APIs.',
                 url='https://risr.hci.utah.edu',
                 author='Research Informatics Shared Resource, Huntsman Cancer Institute, Salt Lake City, UT',
                 author_email='Andrew.Post@hci.utah.edu',
                 package_dir={'': 'src'},
                 packages=['heaobject'],
                 package_data={'heaobject': ['py.typed']},
                 install_requires=[
                     'python-dateutil~=2.8.1',
                     'yarl~=1.5.1'
                 ]
                 )
