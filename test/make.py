from pathlib import Path
import subprocess


def build_and_install(deps=True, extras=None):
    package_root = Path(__file__).parent.parent
    subprocess.run(["python", package_root / "setup.py", "bdist_wheel"], check=True)

    nodeps = ["--no-deps"] if not deps else []
    extras = f"[{','.join(extras)}]" if extras else ""
    wheel_path = next(package_root.glob("dist/*.whl"))
    cmd = ["pip", "install", f"{wheel_path}{extras}",  "--force-reinstall"] + nodeps
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    build_and_install()
