"""Setup the sotamoon module."""
import os
import typing
import shutil

from setuptools import setup, find_packages


def install_requires() -> typing.List[str]:
    """Find the install requires strings from requirements.txt"""
    requires = []
    with open(
        os.path.join(os.path.dirname(__file__), "requirements.txt"), "r"
    ) as requirments_txt_handle:
        requires = [
            x
            for x in requirments_txt_handle
            if not x.startswith(".") and not x.startswith("-e")
        ]
    return requires


def copy_trackers_list():
    """Copy the trackers list."""
    current_dir = os.path.dirname(__file__)
    shutil.copy(
        os.path.join(current_dir, "libraries", "trackerslist", "trackers_all.txt"),
        os.path.join(current_dir, "sotamoon", "fs", "trackers.txt"))


# Run the python setup
copy_trackers_list()
setup(
    name="sotamoon",
    version="0.0.1",
    description="A cryptocurrency that solves for state of the art machine learning models",
    author="Will Sackfield",
    author_email="will.sackfield@gmail.com",
    packages=find_packages(),
    install_requires=install_requires(),
    entry_points={"console_scripts": ["sotamoon=sotamoon.main:main"]},
    include_package_data=True,
)
