import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setuptools.setup(
    name="serverlla", 
    version="1.22",
    author="dylan14567",
    author_email="",
    description="Configure your linux server and check for vulnerabilities with serverlla",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dylan14567/serverlla",
    scripts = ['serverlla'],
    project_urls={
        "Bug Tracker": "https://github.com/dylan14567/serverlla/issues",
    },
    install_requires=[
        "colorama",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="serverlla",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
)
