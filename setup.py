from setuptools import find_packages, setup
import pkg_resources


def load_requirements(path):
    with open(path, encoding="utf-8") as f:
        return [str(req) for req in pkg_resources.parse_requirements(f)]

setup(
    name="mahjong",
    packages=find_packages(),
    package_data={"mahjong": ["resources/rulesets/default.json"]},
    version="0.1.0",
    description="riichi mahjong engine",
    author="Spoogie Oogie",
    license="",
    install_requires=load_requirements("requirements.txt"),
)
