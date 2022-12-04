from setuptools import setup, find_packages
from pynetix import __project__, __version__, __remote__, __description__, __license__

setup(name=__project__,
      version=__version__,
      description=__description__,
      packages=find_packages(),
      license=__license__,
      url=__remote__,
      author='Dominik Brandstetter',
      author_email='brandstetter.dominik@gmx.net',
      install_requires=('pyside6>=6.4.0', 'numpy>=1.23.4',
                        'pyqtgraph>=0.13.1'),
      package_data={'': ['resources/**', ]},
      exclude_package_data={'': ['resources/icons/coloured/*',
                                 'resources/stylesheets/*user*.qss']},
      include_package_data=True)
