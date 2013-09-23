from setuptools import setup

setup(name='taskgda', version='1.0',
      description='OpenShift Python-3.3 Community Cartridge based application',
      author='Ricardo Ocampo', author_email='r.ocampo@itesm.mx',
      url='http://www.python.org/sigs/distutils-sig/',

      #  Uncomment one or more lines below in the install_requires section
      #  for the specific client drivers/modules your application needs.
      install_requires=['CherryPy',
                        'pytz'
                        #  'mysql-connector-python',
                        #  'pymongo',
                        #  'psycopg2',
      ],
     )
