from setuptools import setup, find_packages

setup(
    name="icc.xray",
    version="0.0.2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["icc"],
    scripts = ['src/icc/app.py'],
    install_requires=["setuptools",
                      "zope.component",],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.glade', ],
        }
    )
