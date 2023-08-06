from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required_packages = [
    "getfilelistpy", "lmdb", "matplotlib", "numpy", "Pillow", "pytorch_lightning", "setuptools",
    "six", "torch", "torchvision", "py7zr"
]

setup(
    name="lightningdata-modules",
    version="0.1.8",
    description="Pre-packages Pytorch-Lightning datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ManuelRoeder/lightningdata-modules",
    author="Manuel Roeder",
    author_email="manuel.roeder@web.de",
    license="MIT",
    packages=find_packages(),
    install_requires=required_packages,
    python_requires='>=3.8.12',
    package_data={"": ["README.md", "LICENSE"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ]
)