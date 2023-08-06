""" Set Up """

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='urso',
    version='1.0',
    description='Random Content Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Humberto Barrantes',
    author_email='sudohumberto@gmail.com',
    packages=['urso'],
    install_requires=[
        'cffi==1.15.1',
        'numpy==1.24.3',
        'opencv-python==4.7.0.72',
        'pycparser==2.21',
        'soundfile==0.12.1',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    py_modules=['urso']
)
