from setuptools import setup, find_packages

setup(
    name='controlnet_v11_utils',
    version='0.0.5',
    packages=find_packages(include=['controlnet', 'controlnet/*'])
)