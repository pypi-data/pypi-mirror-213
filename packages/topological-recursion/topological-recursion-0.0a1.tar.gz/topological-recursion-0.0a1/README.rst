# Topological Recursion

`topological-recursion` is a Python module to compute with topological
recursion.

## Installation

### Prerequisites

Make sure that Python 3 is installed in version 3.8 or later.

### Pip installation

To install the module on your system, simply run::

      $ pip install topological-recursion

The above command will download the code from
[PyPI](https://pypi.org/project/topological-recursion/) and then
install on your system.

### Editable installation of the development version

Alternatively, if you want to install the development version, you
need versioning software ``git`` installed. You first need to clone the
project::

    $ git clone https://gitlab.com/toprec/toprec.git

and then run the installation procedure with::

    $ pip install -e toprec/

(the `-e` option makes an editable installation that avoids to
uninstall/install every time you change the files in the library)

### Checking installation

To check whether the installation worked, change repository and try to load
the module with::

    $ python
    >>> import topological_recursion

## Authors and acknowledgment

- V. Delecroix
- B. Eynard
- D. Mitsios

## Aknowledgements

- ERC ReNewQuantum

## License

`topological-recursion` is distributed under the terms of the GNU General
Public License (GPL) published by the Free Software Foundation; either version
2 of the License, or (at your option) any later version.
See http://www.gnu.org/licenses/.
