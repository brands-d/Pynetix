from setuptools import setup
from enzym import __version__, __remote__

setup(name='enzym',
      version=__version__,
      description='Something something organic chemistry.',
      packages=('enzym', ),
      license='GPLv3',
      url=__remote__,
      author='Dominik Brandstetter',
      author_email='brandstetter.dominik@gmx.net',
      install_requires=('PyQt6>=6.4.0', 'numpy>=1.23.4', 'pyqtgraph>=0.13.1'),
      include_package_data=True)
