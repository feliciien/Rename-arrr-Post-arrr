from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Development dependencies
dev_requirements = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.23.2",
    "pytest-qt>=4.2.0",
    "black>=23.12.1",
    "isort>=5.13.2",
    "flake8>=7.0.0",
    "mypy>=1.8.0",
]

setup(
    name="rename_arrr",
    version="1.0.0",
    author="Felicien",
    description="A powerful media file renaming tool with metadata fetching and organization features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/feliciien/Rename-arrr-Post-arrr",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Desktop Environment :: File Managers",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "rename-arrr=rename_arrr.cli:main",
            "rename-arrr-gui=rename_arrr.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "rename_arrr": ["*.md", "*.txt"],
    },
)