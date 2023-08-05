import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages_list = setuptools.find_packages(where="src")


setuptools.setup(
    name="tkxui",
    version="1.1.5",
    author="Martin Gate",
    author_email="martingate98000@gmail.com",
    description="Create modern frameless GUIs with Python, Tkinter and JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GateMartin/TkXUI",
    project_urls={
        "Bug Tracker": "https://github.com/GateMartin/TkXUI/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=packages_list,
    python_requires=">=3.2"
)