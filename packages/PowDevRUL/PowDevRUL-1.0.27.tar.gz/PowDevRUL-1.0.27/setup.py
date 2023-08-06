from setuptools import setup, find_packages


setup(
    name='PowDevRUL',
    version='1.0.27',
    description ='The project aims to assess the lifetime and efficiency of electronic components by using thermal and electrical calculations based on data from an Excel file. Authors: Paul Garnier (paul.garnier@ens-rennes.fr), Briac Baudais (briac.baudais@ens-rennes.fr)',
    readme='README.md',
    license='MIT',
    author='Garnier Paul, Baudais Briac',
    author_email='paul.garnier@ens-rennes.fr, briac.baudais@ens-rennes.fr',
    url='https://github.com/PGarn/LifeTime',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'scipy>=1.10.1',
        'pandas>=2.0.1',
        'matplotlib>=3.7.1',
        'numpy>=1.24.1',
        'rainflow>=3.2.0',
        'openpyxl>=3.1.2',
    ],
)
