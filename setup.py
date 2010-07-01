from setuptools import setup, find_packages

setup(
    name="dispersive",
    version="0.0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["dispersive"],
    install_requires=["setuptools",
                      "zope.component",],
    )
