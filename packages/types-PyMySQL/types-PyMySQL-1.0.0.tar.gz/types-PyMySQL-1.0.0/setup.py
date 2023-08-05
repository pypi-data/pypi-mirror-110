from setuptools import setup

name = "types-PyMySQL"
description = "Typing stubs for PyMySQL"
long_description = '''
## Typing stubs for PyMySQL

This is an auto-generated PEP 561 type stub package for `PyMySQL` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `PyMySQL`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/PyMySQL. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `4d981f87e39371c39b89562364f514291331ba90`.
'''.lstrip()

setup(name=name,
      version="1.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['pymysql-stubs'],
      package_data={'pymysql-stubs': ['times.pyi', 'cursors.pyi', 'converters.pyi', 'util.pyi', 'err.pyi', 'connections.pyi', '__init__.pyi', 'charset.pyi', 'constants/FLAG.pyi', 'constants/CLIENT.pyi', 'constants/SERVER_STATUS.pyi', 'constants/FIELD_TYPE.pyi', 'constants/__init__.pyi', 'constants/ER.pyi', 'constants/COMMAND.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
