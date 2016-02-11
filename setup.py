import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid==1.6.1',
    'pyramid_debugtoolbar',
    'psycopg2==2.6.1',
    'SQLAlchemy==1.0.11',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

excludes= ["utentes.tests", ]

setup(name='utentes',
      version='0.0',
      description='utentes',
      author='iCarto',
      author_email='info@icarto.es',
      url='http://icarto.es',
      packages=find_packages(exclude=excludes),
      include_package_data=True,
      zip_safe=False,
      test_suite='utentes.tests',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = utentes:main
      [console_scripts]
      initialize_utentes_db = utentes.scripts.initializedb:main
      """,
      )
