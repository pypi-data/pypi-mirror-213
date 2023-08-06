from setuptools import setup

setup(name='raster_basics',
      version='1.3.2',
      description='Basic GeoTIFF Processing',
      packages=['raster_basics'],
      author_email='awwells@andrew.cmu.edu',
      url='https://github.com/albinwwells/Raster-Basics',
      zip_safe=False)

# navigate to directory
# python setup.py sdist
# twine upload dist/* 
# awwells, Awells98

# sudo pip install raster_basics --upgrade