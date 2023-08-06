from setuptools import setup

setup(name='cstore',
      version='0.2',
      description='A tools to store and recall useful commands, specifically created to assist forgetful individuals like myself :-)',
      url='https://github.com/navidved/ctore',
      author='Navid Arabi',
      author_email='navidved@gmail.com',
      license='Apache License 2.0',
      packages=['cstore'],
      install_requires=[
          'rich',
      ],
      zip_safe=False)