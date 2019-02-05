# -*- coding: utf-8 -*-

from setuptools import setup
from rchain_keygen import \
    __package__ as main_package, \
    __version__ as current_version

app = '%s.__main__:main' % main_package

setup(
    name=main_package,
    version=current_version,
    author="Paolo D'Onorio De Meo",
    author_email='paolo@proofmedia.io',
    description='Python helper to generate new private/public keys pair to run RChain node as validator',
    license='MIT',
    packages=[main_package],
    python_requires='>=3.5.1',
    entry_points={
        'console_scripts': [
            'rchain-keygen=%s' % app,
        ],
    },
    url='https://pdonorio.github.io/rchain-keys-generator',
    keywords=['rchain', 'blockchain', 'keypairs', 'generator'],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
