# Example Package
This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

# Setup
```{bash}
$ git clone 
```

To install the package locally:

```bash
$ make install
```

To build the wheels and source distributions files:

```bash
$ make build
```

To upload the builded package to PyPI:

```bash
$ make upload
```

In order to build and upload sequentially, you should just:

```bash
$ make pypi
```

# Usage
```python
from example_package_joaopcnogueira import example

example.add_one(10)
```

# Package Structure

> `example_package_joaopcnogueira/`
- The package folder, within it there is the python modules.

> `example_package_joaopcnogueira/__init__.py`
- File that indicates that the folder `example_package_joaopcnogueira` is a package

> `example_package_joaopcnogueira/example.py`
- Python module

> `pyproject.toml`
- File that contains metadata information about the package and how to build it. It's the current recommendation instead of setup.py

> `README.md`
- This actual file, where we put information about the package to be read by humans.

> `.gitignore`
- Git special file which indicates what files and folders should not be tracked by git.

> `Makefile`
- A configuration file which handles command line utilities on how to install, build and upload the project to PyPI.

> `notebooks/`
- Folder where notebooks files exists.

> `tests/`
- Folder where the tests code exists.




# References
[Packaging Python Projects from PyPA - Python Project Authority](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
