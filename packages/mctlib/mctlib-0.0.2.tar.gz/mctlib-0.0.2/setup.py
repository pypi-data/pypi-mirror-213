from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='mctlib',
  version='0.0.2',
  description='some extra functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mate Chocheli',
  author_email='matechocheli2@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mistacheeselib', 
  packages=find_packages(),
  install_requires=[''] 
)

url =""
