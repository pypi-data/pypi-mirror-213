from setuptools import find_packages, setup

with open('README.md') as description:
    description = description.read()

setup(
    name='fake12',
    description=description,
    version="0.0.1",
    long_description_content_type="text/markdown",
    author='Girish Mittapalle',
    author_email='mittapalligirish2001@gmail.com',
    long_description=description,
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False)