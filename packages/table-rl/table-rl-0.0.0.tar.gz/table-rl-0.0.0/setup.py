import codecs
from setuptools import find_packages
from setuptools import setup

install_requires = [
    'gym',
    'numpy>=1.10.4',
    'filelock',
]

test_requires = [
    'pytest',
    'attrs<19.2.0',  # pytest does not run with attrs==19.2.0 (https://github.com/pytest-dev/pytest/issues/3280)  # NOQA
]

setup(name='table-rl',
      version='0.0.0',
      description='table-rl, an online tabular reinforcement learning library',
      long_description=codecs.open('README.md', 'r', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      author='Prabhat Nagarajan',
      author_email='nagarajan@ualberta.ca',
      license='MIT License',
      packages=find_packages(),
      install_requires=install_requires,
      test_requires=test_requires)