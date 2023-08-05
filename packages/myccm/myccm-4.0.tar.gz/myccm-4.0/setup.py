import os
from setuptools import setup

path = os.path.abspath(os.path.dirname(__file__))

try:
  with open(os.path.join(path, 'README.md')) as f:
    long_description = f.read()
except Exception as e:
  long_description = "customize okta cli"

setup(
    name = "myccm",
    version = "4.0",

    description = "this is a causal inference method",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",

    url = "https://github.com/zhougang2020/CCM",
    author = "zhougang",
    author_email = "zg_pem@163.com",

    packages=['src'],
    include_package_data = True,

    platforms = "any",

    scripts = [],
    entry_points = {
        'console_scripts': [
            'okta-cmd=oktacmd:main_cli'
        ]
    }
)