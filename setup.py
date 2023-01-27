from setuptools import setup, find_packages

_packages = []

for package in find_packages():
    if package.startswith('amir_dev_studio_tests'):
        continue
    _packages.append(package)

setup(
    name='amir-dev-studio',
    version='0.0.2',
    packages=_packages,
    install_requires=[]
)
