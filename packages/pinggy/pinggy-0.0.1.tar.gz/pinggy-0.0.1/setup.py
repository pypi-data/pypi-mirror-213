from setuptools import setup, find_packages


setup(
    name='pinggy',
    version='0.0.1',
    license='MIT',
    author="Abhijit Mondal",
    author_email='am@abhijitmondal.in',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/abhimp/pinggypython',
    keywords='tunnel, file share',
    install_requires=[
          'paramiko',
      ],

)