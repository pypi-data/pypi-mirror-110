from os import EX_TEMPFAIL
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wallaroo",
    version='0.0.17',
    url="https://www.wallaroo.ai/",
    author="Wallaroo.ai",
    author_email="hello@wallaroo.ai",
    license="UNKNOWN",
    description='Wallaroo.ai model management API client',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules=["sdk"],
    package_dir={'': '.'},
    packages=setuptools.find_packages(exclude=["tests", "wallaroo_upcoming"]),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       "google-cloud-storage >= 1.38.0",
       "onnx >= 1.8.0"
   ],
    python_requires=">=3.7",
)
