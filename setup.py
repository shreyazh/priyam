from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="priyam",
    version="1.0.1",
    author="justshreyash",
    author_email="usershreyash@gmail.com",
    description="A comprehensive Python package for mathematical operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shreyazh/priyam",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/shreyazh/priyam/issues",
        "Source": "https://github.com/shreyazh/priyam",
        "Documentation": "https://github.com/shreyazh/priyam/docs",
    },
)