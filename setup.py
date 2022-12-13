from setuptools import find_packages, setup
import pkg_resources

with open("requirements.txt", encoding="utf-8") as f:
    install_requires = [str(req) for req in pkg_resources.parse_requirements(f)]

setup(
    name="mahjong",
    packages=find_packages(),
    package_data={"mahjong": ["resources/rulesets/default.json"]},
    version="0.1.0",
    description="riichi mahjong engine",
    author="Spoogie Oogie",
    license="",
    install_requires=install_requires,
)
