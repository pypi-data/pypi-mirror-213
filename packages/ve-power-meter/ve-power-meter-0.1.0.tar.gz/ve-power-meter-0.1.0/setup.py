from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="ve-power-meter",
    version="0.1.0",
    description="Power meeasurement tool for the NEC Vector Engine",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="http://github.com/keichi/ve-power-meter",
    author="Keichi Takahashi",
    author_email="hello@keichi.dev",
    license="MIT",
    packages=["ve_power_meter"],
    entry_points={
        "console_scripts": [
            "ve-power-meter = ve_power_meter:main"
        ]
    }
)
