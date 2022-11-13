from setuptools import setup, find_packages
from pynetix import __project__, __version__, __remote__, __description__

setup(name='pynetix',
      version=__version__,
      description=__description__,
      packages=find_packages(),
      license='GPLv3',
      url=__remote__,
      author='Dominik Brandstetter',
      author_email='brandstetter.dominik@gmx.net',
      install_requires=('PyQt6>=6.4.0', 'numpy>=1.23.4', 'pyqtgraph>=0.13.1'),
      include_package_data=True)
