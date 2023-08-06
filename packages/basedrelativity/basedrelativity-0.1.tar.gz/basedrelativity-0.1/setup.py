from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name='basedrelativity',
  version='0.1',
  description='Solve relativity problems and actually get the right answer.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='basedphysics',
  author_email='contact@basedphysics.com',
  license='MIT',
  url='http://github.com/basedphysics/basedrelativity',
  packages=['basedrelativity'],
  install_requires=[
    # 'dependency>=1.0',
  ],
  python_requires='>=3.8',
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
  ],
)
