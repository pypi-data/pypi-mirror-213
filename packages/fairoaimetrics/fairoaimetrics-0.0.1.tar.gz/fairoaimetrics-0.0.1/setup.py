from setuptools import setup

setup(
    name="fairoaimetrics",
    version="0.0.1",  # TODO <- get me automatically somehow.
    author="Fairo Systems, Inc.",
    author_email="support@fairo.ai",
    description=("A collection of pre-certified fairness metrics supported by Fairo."),
    license="Apache-2.0",
    keywords="fairo fairness AI governance metrics",
    url="http://www.fairo.ai",  # TODO <- once im on pypy put the real URL here.
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=['fairo-metrics'],
    install_requires=[],
)
