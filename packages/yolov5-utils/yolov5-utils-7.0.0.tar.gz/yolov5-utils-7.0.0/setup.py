import io
import os
import re

import setuptools


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "yolov5_utils", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


setuptools.setup(
    name="yolov5-utils",
    version=get_version(),
    author="",
    license="GPL",
    description="Packaged version of the Yolov5 object detector",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/msclock/yolov5-utils",
    packages=setuptools.find_packages(exclude=["tests"])
    + [
        "yolov5_utils.yolov5.utils",
        "yolov5_utils.yolov5.classify",
        "yolov5_utils.yolov5.segment",
    ],
    python_requires=">=3.7",
    install_requires=get_requirements(),
    include_package_data=True,
    options={"bdist_wheel": {"python_tag": "py37.py38.py39.py310"}},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    keywords="machine-learning, deep-learning, ml, pytorch, YOLO, object-detection, vision, YOLOv5, YOLOv7",
    entry_points={
        "console_scripts": [
            "yolov5_cli=yolov5_utils.cli:app",
        ],
    },
)
