import importlib.util
from setuptools import setup, find_packages
from pathlib import Path


root = Path(__file__).absolute().parent

with root.joinpath("README.md").open() as fh:
    long_description = fh.read()

spec = importlib.util.spec_from_file_location("curricula", str(root.joinpath("curricula")))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

setup(
    name="curricula",
    version=module.__version__,
    description="A content manager and grading toolkit for evaluating student code",
    url="https://github.com/curriculagg/curricula",
    author="Noah Kim",
    author_email="noahbkim@gmail.com",

    # Extra
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Python
    python_requires=">=3.7",

    # Packaging
    packages=find_packages(),
    package_data={"curricula": [
        "compile/schema/*.json",
        "grade/include/*.hpp",
        "grade/include/**/*.hpp",
        "grade/gtest/*.cpp",
        "template/**/*.md",
        "template/**/*.html"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=["jinja2", "jsonschema"])