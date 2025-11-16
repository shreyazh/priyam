from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Only include main production dependencies from requirements.txt
def parse_requirements(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#") \
                and not any(line.startswith(dev_pkg) for dev_pkg in [
                    "pytest", "pytest-cov", "black", "flake8", "sphinx", "sphinx-rtd-theme", "requests", "beautifulsoup4", "playwright", "lxml", "opencv-python", "pytesseract", "Pillow", "yt-dlp", "scikit-image", "tk", "reportlab"
                ])]

setup(
    name="priyam",
    version="0.0.1",
    author="justshreyash",
    author_email="usershreyash@gmail.com",
    description="Comprehensive suite for Math, Physics, Chemistry, Computer Science, Algorithms, Utilities, Desktop GUI tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shreyazh/priyam",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    install_requires=parse_requirements("requirements.txt"),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "requests",
            "beautifulsoup4",
            "playwright",
            "lxml",
            "opencv-python",
            "pytesseract",
            "Pillow",
            "yt-dlp",
            "scikit-image  ",
            "tk",
            "reportlab"
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/shreyazh/priyam/issues",
        "Source": "https://github.com/shreyazh/priyam",
        "Documentation": "https://github.com/shreyazh/priyam/docs",
    },
)