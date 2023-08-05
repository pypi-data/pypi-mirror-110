from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="pywasher",
    version="1.3.1",
    description="pywasher",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/jeroenclappform/pywasher",
    download_url = 'https://github.com/jeroenclappform/pywasher/archive/1.3.1.tar.gz',
    author="StanBekker",
    author_email="s.bekker@clappform.com",
    keywords="dataframe cleaner",
    license="MIT",
    packages = ['pywasher'],
    install_requires=[
        "pandas"
    ],
    include_package_data=True,
)