from setuptools import setup, find_namespace_packages


with open("README.md", "r") as file_handler:
    long_description = file_handler.read()

main_ns = {}
with open("qurix/data/catalog/__version__.py", "r") as file_handler:
    exec(file_handler.read(), main_ns)

setup(
    name="qurix-data-catalog",
    version=main_ns["VERSION"],
    author="qurix Technology",
    description="Client for the qurix Data Catalog for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qurixtechnology/python-package-template",
    packages=find_namespace_packages(),
    install_requires=[
    ],
    extras_require=dict(
        dev=[
            "pytest==7.3.1",
            "flake8==6.0.0",
            "pytest-flake8==1.1.1",
            "pytest-cov==4.0.0",
            "wheel==0.40.0",
            "twine==4.0.2",
        ]
    ),
    python_requires=">=3.10",
    keywords=["python"],
)
