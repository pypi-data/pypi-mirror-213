# PyScanner
PyScanner is a python library for security reconnaissance

## Installation

### Setup tool install

```bash
python setup.py sdist
python setup.py install
```

### Pip install

```bash
python setup.py sdist
pip install .
```

### Pip uninstall

```bash
pip uninstall pyscanner

```


## Usage
### Ftp scanner

```python
from pyscanner.ftp.ftp_scanner import *


scanner = FtpScanner(max_thread=10,timeout=2)
returns = scanner.scan("2.2.2.2","2.2.3.3") #startip, endip

for ip in returns:
    print(ip)

```

