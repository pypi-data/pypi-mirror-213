from setuptools import setup, find_packages

setup(
    author="Subhradeep Rang",
    author_email="srang992@gmail.com",
    name="custom_flet",
    version="0.1.3",
    description="package containing custom flet controls for ease of use.",
    packages=find_packages(include=['custom_flet', 'custom_flet.*']),
)
