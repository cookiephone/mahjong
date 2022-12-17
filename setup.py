from pathlib import Path
from setuptools import find_packages, setup
import pkg_resources


def load_requirements(path):
    with open(path, encoding="utf-8") as f:
        return [str(req) for req in pkg_resources.parse_requirements(f)]


if __name__ == "__main__":
    package_root = Path(__file__).parent
    setup(
        name="mahjong",
        dist_dir=package_root,
        build_base=package_root,
        egg_base=package_root,
        packages=find_packages(package_root),
        package_dir={
            "": str(package_root),
        },
        package_data={
            "mahjong": ["resources/rulesets/default.json"],
            "visualizer": ["resources/**/*.*"],
        },
        version="0.1.0",
        description="riichi mahjong engine",
        author="Spoogie Oogie",
        license_files=[str(package_root / "license.md")],
        install_requires=load_requirements(package_root / "requirements.txt"),
        extras_require={
            "dev": load_requirements(package_root / "requirements-dev.txt"),
        },
    )
