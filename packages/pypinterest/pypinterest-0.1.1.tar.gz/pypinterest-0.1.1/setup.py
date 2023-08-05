"""
Pinterest Client Package Setup
"""
import os
from datetime import datetime
from pathlib import Path
from setuptools import setup, find_namespace_packages


def _get_test_version():
    return datetime.today().strftime('%m%d%Y%H%M%S')


def _get_prod_version():
    module = {}
    with open(os.path.join(package_root, "pypinterest/utils/version.py"), encoding='UTF-8') as fp:
        exec(fp.read(), module)  # pylint: disable=exec-used
    return module.get("__version__")


_IS_TEST_BUILD = os.environ.get("IS_TEST_BUILD", 0)

REQUIRES = []

long_description = (Path(__file__).parent / "README.md").read_text()
package_root = os.path.abspath(os.path.dirname(__file__))

__version__ = None

if _IS_TEST_BUILD:
    print("* Test build enable")
    __version__ = _get_test_version()
else:
    __version__ = "0.0.3"

if __version__ is None:
    raise ValueError("Version is not defined")

setup(
    name="pypinterest",
    description="Pinterest API",
    version= "0.1.1",
    author="Techfarm",
    author_email="tamilcomway@gmail.com",
    url="https://github.com/piriyaraj/pypinterest",
    install_requires=REQUIRES,
    include_package_data=True,
    packages=find_namespace_packages(
        include=['pinterest.*', 'pinterest', 'pinterest.version', 'pinterest.config'],
        exclude=[
            'sample',
            'sample.*',
            'tests',
            'tests.*',
            'integration_tests',
            'integration_tests.*',
            '.github',
        ]
    ),
    license='Apache License 2.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
)