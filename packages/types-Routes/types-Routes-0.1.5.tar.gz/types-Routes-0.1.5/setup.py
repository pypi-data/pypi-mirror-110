from setuptools import setup

name = "types-Routes"
description = "Typing stubs for Routes"
long_description = '''
## Typing stubs for Routes

This is an auto-generated PEP 561 type stub package for `Routes` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Routes`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Routes. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `bc2ec748f68dcb516a9ed83c6b8a494f31cf3698`.
'''.lstrip()

setup(name=name,
      version="0.1.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['routes-python2-stubs'],
      package_data={'routes-python2-stubs': ['mapper.pyi', 'util.pyi', '__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
