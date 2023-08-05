from setuptools import setup
import os

tag = os.getenv('CI_COMMIT_TAG')

if tag:
    version = tag
else:
    version = '0.1.0'

setup(
    name='icap_commons',
    version=version,
    description='Example Python library',
    author='Makrand Bhonde',
    author_email='makrand.bhonde@bluealtair.com',
    packages=['icap_commons'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)