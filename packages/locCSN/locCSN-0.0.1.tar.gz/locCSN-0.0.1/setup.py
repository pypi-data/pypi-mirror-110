"""Setup for the locCSN package."""

import setuptools

setuptools.setup(
    author="Xuran Wang",
    author_email="xuranw@andrew.cmu.edu",
    name='locCSN',
    license="MIT",
    description='locCSN is a python package for local cell specific networks.',
    version='0.0.1',
    url='https://github.com/xuranw/locCSN',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)