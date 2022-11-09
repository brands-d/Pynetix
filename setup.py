from setuptools import setup, find_packages
from enzym import __version__

setup(name='enzym',
      version=__version__,
      description='Something something organic chemistry.',
      packages=('src', ),
      license='GPLv3',
      # url='https://github.com/brands-d/kMap',
      author='Dominik Brandstetter',
      author_email='brandstetter.dominik@gmx.net',
      install_requires=('PyQt6>=6.4.0', 'numpy>=1.23.4', 'pyqtgraph>=0.13.1'),
      include_package_data=True)
