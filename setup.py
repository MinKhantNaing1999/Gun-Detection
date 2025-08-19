from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "Gun Detection",
    version = "1.0",
    author = "Min Khant Naing",
    email = "minkhantnaing344@gmail.com",
    packages = find_packages(),
    install_requires = requirements,
)