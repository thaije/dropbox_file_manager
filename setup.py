from setuptools import find_packages, setup

setup(
    name="dropbox_file_manager",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    description="Simple Python package that uses the dropbox API to upload files and pass back a download link.",
    author="Tjalling Haije",
    author_email="tjalling_haije@outlook.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        # PUT YOUR PYTHON DEPENDENCIES HERE. E.g.:
        "dropbox==11.*"
        # ...
    ],
)
