# -*- coding: utf-8 -*-
from setuptools import setup
from io import open

def readme():
    with open('README.md', encoding="utf-8-sig") as f:
        README = f.read()
    return README


setup(
    name='focalnet-tf',
    version='0.0.1',    
    description='Re-implementation of FocalNet for tensorflow 2.X',
    author='Shiro-LK',
    author_email='shirosaki94@gmail.com',
    license='MIT License',
    packages=['focalnet'],
    package_data={'focalnet': ['imagenet-1k.json', 'imagenet-21k.json', 'imagenet-22k-reorder.json']},
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=['numpy', 
                      "pytest", "tensorflow", "opencv-python"
                      ],
    url='https://github.com/Shiro-LK/focalnet-tf',
    download_url='https://github.com/Shiro-LK/focalnet-tf.git',
    keywords=["focalnet", "tensorflow"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
