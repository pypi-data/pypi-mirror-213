import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["requests>=2.31.0"]

setuptools.setup(
    name="jloader",
    version="0.0.5",
    author="Lojaleto",
    author_email="lojaleto@yandex.ru",
    description="Downloader for jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lojaleto/jloader",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)