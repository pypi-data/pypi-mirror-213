import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "iosense_connect",
    version = "4.0.0",
    author = "Faclon-Labs",
    author_email = "reachus@faclon.com",
    description = "iosense connect library",
    packages = ["iosense_connect"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=[
        'numpy',
        'pandas',
        'pyarrow',
        'requests',
        'azure-storage-blob',
        'azure-core',
        'pytz',
        'fsspec',
        'gcsfs',
        's3fs'
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
