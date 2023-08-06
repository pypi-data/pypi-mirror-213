from setuptools import setup, find_packages

setup(
    name="InfixToPostfix",
    version="1.0.7",
    author="RoiexLee",
    author_email="luoyixaun1029@gmail.com",
    description="A python module converts infix expressions to postfix expressions and includes a visual interface.",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    url="https://github.com/RoiexLee/InfixToPostfiX",
    packages=find_packages(),
    python_requires=">=3.11.0",
    install_requires=open("requirements.txt").read().split("\n"),
    include_package_data=True
)
