# -*- coding: utf-8 -*-

# Distributing: https://packaging.python.org/en/latest/distributing/
# To register for pip create PKG-INFO with python setup.py egg_info

from setuptools import setup, find_packages


with open("README", "r") as fp:
    long_description = fp.read()


setup(name='andado',
      version='0.0.1',
      description="Reconstruct where you've been by looking at your photos",
      long_description=long_description,
      author='Juan Reyero',
      author_email='juan@juanreyero.com',
      # url='http://example.com/pysample/',
      # py_modules=['andado'],
      packages=find_packages('.', exclude=['*.test']),
      entry_points={'console_scripts':
                    ['andado = andado.traverse:main',
                     'photocp = andado.photo:main_photocp',
                     'photoimport = andado.photo:main_photoimport']},
      # package_data={'andado': ['res/diagonal.npy', 'res/*.txt']},
      # install_requires=[  # 'numpy>=1.9.0'
      #     'dateutil>=1.5'
      # ],
      # Classifiers: https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=["Programming Language :: Python :: 2",
                   # "Programming Language :: Python :: 3",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: Apache Software License",
                   "Topic :: Scientific/Engineering",
                   "Topic :: Software Development :: Libraries"])
