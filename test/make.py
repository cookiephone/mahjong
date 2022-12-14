from pathlib import Path
import subprocess


def build_and_install(deps=True, extras=None):
    package_root = Path(__file__).parent.parent
    cmd = [
        "python", package_root / "setup.py",
        "bdist_wheel", "--dist-dir", package_root / "dist",
        "build", "--build-base", package_root / "build",
        "egg_info", "--egg-base", package_root / "build",
    ]
    subprocess.run(cmd, check=True)

    nodeps = ["--no-deps"] if not deps else []
    extras = f"[{','.join(extras)}]" if extras else ""
    wheel_path = next(package_root.glob("dist/*.whl"))
    cmd = ["pip", "install", f"{wheel_path}{extras}",  "--force-reinstall"] + nodeps
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    build_and_install()
