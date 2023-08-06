from setuptools import setup, find_packages

setup(name="client_chat69",
      version="0.1.1",
      description="Client 'Async chat' application",
      author="nikyshu",
      author_email="nikyshu@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', ]
      )

# python setup.py sdist bdist wheel
