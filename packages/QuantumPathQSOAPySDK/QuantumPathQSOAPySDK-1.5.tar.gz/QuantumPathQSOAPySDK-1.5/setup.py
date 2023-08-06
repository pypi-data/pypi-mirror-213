from setuptools import setup, find_packages

classifiers = [
  'Topic :: Scientific/Engineering',
  'Topic :: Software Development',
  'Development Status :: 5 - Production/Stable',
  'License :: Freely Distributable',
  'License :: Other/Proprietary License',
  'Programming Language :: Python :: 3',
  'Operating System :: OS Independent',
  'Intended Audience :: Developers',
  'Intended Audience :: Education',
  'Intended Audience :: Information Technology'
]

setup(
  name='QuantumPathQSOAPySDK',
  version='1.5',
  description='QuantumPath qSOA Python SDK',
  long_description=open('README.md').read(),
  long_description_content_type = 'text/markdown',
  url='https://core.quantumpath.app/',
  author='QuantumPath',
  classifiers=classifiers,
  keywords='quantum, quantumpath, qSOA, sdk, quantum applications, quantum software',
  packages=find_packages(exclude=["test"]),
  install_requires=['requests', 'matplotlib', 'prettytable']
)