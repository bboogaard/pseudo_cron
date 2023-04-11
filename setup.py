from setuptools import setup, find_packages
from pseudo_cron.version import Version


setup(name='pseudo_cron',
     version=Version('1.0.0').number,
     description='Pseudo cron for Django',
     long_description=open('README.md').read().strip(),
     long_description_content_type="text/markdown",
     author='Bram Boogaard',
     author_email='padawan@hetnet.nl',
     url='https://github.com/bboogaard/pseudo_cron',
     packages=find_packages(include=['pseudo_cron', 'pseudo_cron.migrations', 'pseudo_cron.service']),
     install_requires=[
         'pytest',
         'pytest-cov',
         'pytest-django==4.5.2',
         'django==3.2'
     ],
     license='MIT License',
     zip_safe=False,
     keywords='Django cron',
     classifiers=['Development Status :: 3 - Alpha'])
