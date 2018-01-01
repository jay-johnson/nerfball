import os
import sys
import warnings
import unittest

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py


cur_path, cur_script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(cur_path))

install_requires = [
    "ansible>=1.9",
    "pep8>=1.7.1",
    "flake8>=3.4.1",
    "boto3",
    "pycurl",
    "celery-connectors",
    "logstash-formatter",
    "python-logstash",
    "docker-compose",
    "coverage",
    "future",
    "pylint",
    "unittest2",
    "mock"
]


if sys.version_info < (3, 5):
    warnings.warn(
        "Less than Python 3.5 is not supported.",
        DeprecationWarning)


def nerfball_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


# Don"t import nerfball module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "nerfball"))

setup(
    name="nerfball",
    cmdclass={"build_py": build_py},
    version="1.0.0",
    description="IoT Nerfball",
    long_description="" +
    "This repository was built as a thought experiment in learning how to " +
    "defend against attacks and exploits from python-based threats. I " +
    "built this specifically to learn how internet chemotherapy worked and " +
    "how to defend against it. I hope others will find it valuable when " +
    "they try to defend against something like this in the future. " +
    "After reviewing how the code worked, I built a jail to help me " +
    "nerf what I didn't need. By disabling the system's python calls " +
    "the container has a reduced surface area for this type of " +
    "application to do something bad. Please note, even the approach " +
    "outlined in this repository is not perfect for all types of " +
    "threats or new ones in the future. " +
    "I did not know of a tool to inspect hacks like this where " +
    "untrusted code was in play that could easily destroy my own " +
    "property if I screwed up. This repository is how I built " +
    "the jail and crafted it to inspect the python system calls as they " +
    "ran on the host operating system. After the system access audit " +
    "passed the unittests, I started to feel comfortable that " +
    "I could debug with less chance of something going bad " +
    "while learning how the code worked.",
    author="Jay Johnson",
    author_email="jay.p.h.johnson@gmail.com",
    url="https://github.com/jay-johnson/nerfball",
    packages=[
        "nerfball",
        "nerfball.importlib",
        "nerfball.log"
    ],
    package_data={},
    install_requires=install_requires,
    test_suite="setup.nerfball_test_suite",
    tests_require=[
    ],
    scripts=[
        "./nerfball/scripts/listen-on-port.py",
        "./nerfball/scripts/nerf-virtualenv.sh",
        "./nerfball/scripts/dev-nerf.sh"
    ],
    use_2to3=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
