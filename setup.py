"""
Setup script for the code obfuscator package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="code-obfuscator",
    version="1.0.0",
    author="Samir Djili",
    author_email="ns_djili@esi.dz",
    description="A powerful, modular code obfuscation tool supporting multiple programming languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samir-djili/obfuscator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "memory-profiler>=0.58.0",
        ],
        "web": [
            "flask>=2.0.0",
            "flask-cors>=3.0.0",
        ],
        "config": [
            "pyyaml>=5.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "obfuscator=obfuscator:main",
        ],
    },
    keywords="obfuscation, code protection, security, python, javascript, java",
    project_urls={
        "Bug Reports": "https://github.com/samir-djili/obfuscator/issues",
        "Source": "https://github.com/samir-djili/obfuscator",
        "Documentation": "https://github.com/samir-djili/obfuscator/wiki",
    },
    include_package_data=True,
    zip_safe=False,
)
