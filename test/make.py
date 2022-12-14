from pathlib import Path
import subprocess


def build_and_install(deps=True):
    package_root = Path(__file__).parent.parent
    subprocess.run(["python", package_root / "setup.py", "bdist_wheel"], check=True)

    nodeps = ["--no-deps"] if not deps else []
    wheel_path = next(package_root.glob("dist/*.whl"))
    subprocess.run(["pip", "install", wheel_path,  "--force-reinstall"] + nodeps, check=True)


if __name__ == "__main__":
    build_and_install()
