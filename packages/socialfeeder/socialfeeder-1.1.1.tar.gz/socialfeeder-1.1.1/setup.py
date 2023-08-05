from setuptools import setup
from setuptools import find_packages
from socialfeeder import __VERSION__

install_requires = []
with open("requirements.txt", "r") as f:
  content = f.read()
  install_requires.extend(content.splitlines())

setup(
     name='socialfeeder',
     version=__VERSION__,
     author='datnguye',
     author_email='datnguyen.it09@gmail.com',
     packages=find_packages(),
    include_package_data=True,
     url='https://github.com/datnguye',
     license='MIT',
     description='A package to feed things on social',
     long_description_content_type="text/markdown",
     long_description=open('README.md').read(),
     install_requires=install_requires,
     python_requires='>=3.7.5',
     entry_points = {
        'console_scripts': [
            'feeder = socialfeeder.__main__:main'
        ],
    }
)