from setuptools import setup, find_packages

setup(name='mosaik_fmi',
      version='1.0',
      description='Adapter for FMUs (ME or CS) in mosaik',
      long_description='\n\n'.join(
        open(f, 'rb').read().decode('utf-8')
        for f in ['README.rst', 'CHANGELOG', 'AUTHORS.txt']),
      author='Cornelius Steinbrink',
      author_email='mosaik@offis.de',
      url='https://mosaik.offis.de',
      install_requires=[
            'mosaik-api>=2.0',
            'fmipp',
            'mosaik',
            'pytest',
      ],
      packages=find_packages(exclude=['tests*']),
      include_package_data=True,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
