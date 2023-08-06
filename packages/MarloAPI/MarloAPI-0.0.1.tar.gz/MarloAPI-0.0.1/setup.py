from setuptools import setup, find_packages

setup(
    name="MarloAPI",
    version="0.0.1",
    author="2Milan",
    author_email="4lish.net@gmail.com",
    description="A library for working witch Marlo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests"
    ]
)
