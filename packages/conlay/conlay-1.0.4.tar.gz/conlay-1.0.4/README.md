Conlay - Console Layout
=======================

[![PyPi version][shields-pypi_version]][url-pypi_version]
[![Github Issues][shields-issues]][url-issues]
[![Github License][shields-license]][url-license]

Create visually pleasing console layouts with this easy-to-use Python library. 


Installing
----------

Install using <a href="https://pip.pypa.io/en/stable/">pip</a>

```bash
pip install conlay
```

or install it from <a href="https://pypi.org/project/conlay/#files">PyPi</a>


Example
-------

```python
from conlay import *

layout = Conlay()

blank_box = BoldBox(0, 0, 30, 5)
layout.add(blank_box)

label = ThinLabel(0, 0, "this is a test")
blank_box.add(label)

layout.print()
``` 





<!-- shields -->
[shields-pypi_version]: https://img.shields.io/pypi/v/conlay?label=PyPi%20Version&style=for-the-badge
[shields-issues]: https://img.shields.io/github/issues/Salliii/conlay?style=for-the-badge
[shields-license]: https://img.shields.io/github/license/Salliii/conlay?style=for-the-badge

<!-- url -->
[url-pypi_version]: https://pypi.org/project/conlay/
[url-issues]: https://github.com/Salliii/conlay/issues
[url-license]: https://github.com/Salliii/conlay/blob/main/LICENSE