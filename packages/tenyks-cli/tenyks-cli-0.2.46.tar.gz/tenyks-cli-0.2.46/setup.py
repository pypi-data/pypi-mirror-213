from setuptools import find_packages, setup

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().split("\n")

setup(
    name="tenyks-cli",
    version="0.2.46",
    author="Tenyks AI",
    author_email="info@tenyks.ai",
    license="MIT",
    description="Tenyks AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.tenyks.ai/",
    py_modules=["tenyks"],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        tenyks=tenyks.cli:commands
    """,
)
