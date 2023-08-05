from setuptools import setup, find_packages

exec(open("NCBIQuery/version.py").read())

setup(
    name='NCBIQuery',
    version=__version__,
    license='Delt4',
    author="Leo Sun",
    author_email='zidaneandmessi@gmail.com',
    packages=['NCBIQuery'],
    url='https://github.com/nachovy/NCBIQuery',
    keywords='NCBI',
    install_requires=[
          'requests',
          'tokenizers',
      ],

)