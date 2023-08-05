from setuptools import setup, find_packages

setup(
    name="mapbot_frontend",
    version="0.1.6",
    description="A frontend package for MapBot",
    author="Martin Weiss",
    packages=find_packages(),
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
