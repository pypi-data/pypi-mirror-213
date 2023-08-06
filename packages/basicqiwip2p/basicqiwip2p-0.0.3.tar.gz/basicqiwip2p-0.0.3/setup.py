from setuptools import setup

setup(
      name='basicqiwip2p',
      version='0.0.3',
      description='Basic set of tools for working with QiwiP2P',
      url='https://github.com/MaYn3r/BasicQiwiP2P',
      packages=['basicqiwip2p'],
      dependencies = ['httpx', 'pydantic'],
      author_email='mayneryt@bk.ru',
      zip_safe=False
)