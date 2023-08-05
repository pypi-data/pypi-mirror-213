from setuptools import setup, find_packages

setup(
    name="hmd-lang-local-librarian",
    version="0.0.1",
    license="unlicensed",
    package_data={"hmd_lang_local_librarian": ["schemas/**/*.hms"]},
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
