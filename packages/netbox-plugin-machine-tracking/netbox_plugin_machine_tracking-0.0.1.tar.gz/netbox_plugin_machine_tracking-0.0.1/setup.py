from setuptools import find_packages, setup

setup(
    name='machine-tracking',
    version='0.1',
    description='A tool for tracking and logging machine hardware failures and state changes',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
