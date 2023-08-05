import json
from setuptools import setup, find_packages

NAME = "isilon-sdk-thaonv"
VERSION = ""
REQUIRES = ["urllib3 == 1.26.15", "six >= 1.10", "certifi", "python-dateutil"]

with open('version_config.json') as f:
    VERSION = json.load(f).get("sdk_version")


setup(
    name=NAME,
    version=VERSION,
    description="Python language bindings for managing OneFS clusters.",
    maintainer="Isilon SDK",
    maintainer_email="sdk@isilon.com",
    author="Isilon SDK",
    author_email="sdk@isilon.com",
    url="https://github.com/Isilon/isilon_sdk_python",
    keywords=["Swagger", "Isilon SDK", "OneFS", "PowerScale"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    project_urls={
        "Source code": "https://github.com/Isilon/isilon_sdk",
        "Documentation": "https://github.com/Isilon/isilon_sdk_python",
    },
    license='MIT',
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=2.7',
)
