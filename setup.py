# tox requires this to find files in the current dir
__import__("setuptools").setup(
    name="napari-plugin-tests", install_requires=["pydantic", "PyYAML", "tox"]
)
