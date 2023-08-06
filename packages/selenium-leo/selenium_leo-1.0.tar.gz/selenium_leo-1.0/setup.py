from distutils.core import setup

readme = open("./README.md", "r")

setup(name='selenium_leo',
      version='1.0',
      description='Funciones utiles de selenium para uso personal',
      long_description=readme.read(),
      author='Leo',
      author_email='amazongalindo@gmail.com',
      url='https://github.com/silverxd20/selenium_functions',
      packages=['selenium_functions'],
     )