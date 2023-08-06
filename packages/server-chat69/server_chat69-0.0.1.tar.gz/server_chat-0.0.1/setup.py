from setuptools import setup, find_packages

setup(name="server_chat69",
      version="0.0.1",
      description="Server 'Async chat' application",
      author="nikyshu",
      author_email="nikyshu@mail.ru",
      packages=find_packages(),
      install_requires=['sqlalchemy', ]
      )

# python setup.py sdist bdist wheel
