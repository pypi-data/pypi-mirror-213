from setuptools import setup, find_packages

# Open the README file.
with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

setup(
    name='irvy',
    version='1.0.2',
    description='A brief description of your project',  # add this
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),  # this should automatically find your packages
    include_package_data=True,
    install_requires=[
        # list of dependencies
    ],
    entry_points={
        'console_scripts': [
            'irvy=irvy.irvy:main',
        ],
    },
)
