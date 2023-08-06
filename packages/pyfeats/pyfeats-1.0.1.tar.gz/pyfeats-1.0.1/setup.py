from setuptools import setup, find_packages
import os

try:
    long_description = open('README.md', encoding='utf-8').read()
except:
    long_description = open('README.md').read()

classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Libraries',
        "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

setup(
    name="pyfeats",
    version='1.0.1',
    description='Open-source software for image feature extraction',
    long_description= long_description,
    long_description_content_type = 'text/markdown',
    author="Nikolaos G. Giakoumoglou",
    author_email="<nikolaos.giakoumoglou@gmail.com>",
    license='MIT',
    platforms = ['Any'],
    classifiers=classifiers,
    url='https://github.com/giakou4/pyfeats', 
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=['opencv-python', 'numpy', 'scikit-image', 'matplotlib', 'scipy', 'PyWavelets', 'mahotas'],
    keywords=['python', 'image', 'region-of-interest', 'mask', 'features', 'polygon'],
    
)