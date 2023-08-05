import setuptools
import subprocess

try:
    version = (
        subprocess.check_output(["git", "describe", "--abbrev=0", "--tags"])
        .strip()
        .decode("utf-8")
    )
except Exception:
    print("Could not get version tag. Defaulting to version 0")
    version = "0"


if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="acellera-envlicenses",
        version=version,
        description="envlicenses",
        long_description=long_description,
        zip_safe=False,
        url="https://www.htmd.org",
        maintainer="Acellera Ltd",
        maintainer_email="info@acellera.com",
        packages=setuptools.find_packages(include=["envlicenses*"]),
        package_data={"envlicenses": ["permissive.txt"]},
        entry_points={"console_scripts": ["envlicenses = envlicenses:main"]},
    )
