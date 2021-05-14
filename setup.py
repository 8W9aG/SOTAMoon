"""Setup the sotamoon module."""
import os

from setuptools import setup, find_packages

INSTALL_REQUIRES = []
with open(
    os.path.join(os.path.dirname(__file__), "requirements.txt"), "r"
) as requirments_txt_handle:
    INSTALL_REQUIRES = [
        x
        for x in requirments_txt_handle
        if not x.startswith(".") and not x.startswith("-e")
    ]

setup(
    name="sotamoon",
    version="0.0.1",
    description="A cryptocurrency that solves for state of the art machine learning models",
    author="Will Sackfield",
    author_email="will.sackfield@gmail.com",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["sotamoon=sotamoon.main:main"]},
)
