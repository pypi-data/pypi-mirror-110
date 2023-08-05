import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybalancer",
    version="1.0",
    author="Qingfu Wen",
    author_email="qingfu.wen@gmail.com",
    description="an simple load balancer for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wenqf11/pybalancer",
    packages=setuptools.find_packages(),
    install_requires=['uhashring>=2.1'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)