from setuptools import setup, find_packages

# readme_generator/
# ├── setup.py
# ├── README.md
# ├── requirements.txt
# ├── readme_generator/
# │   ├── __init__.py
# │   ├── cli.py
# │   ├── core.py
# │   ├── tools.py
# │   └── config.py
# └── tests/
#     └── test_readme_generator.py

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="crewai-readme-generator",
    version="0.1.0",
    author="Sarthak Dargan",
    author_email="sarthak221995@gmail.com",
    description="A CrewAI-powered tool to generate comprehensive README files for GitHub repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crewai-readme-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "readme-gen=readme_generator.cli:main",
            "crewai-readme=readme_generator.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "readme_generator": ["templates/*.md"],
    },
)