Garmin Aviation Checklist Editor (ACE) - Python Module
======================================================

Parse and write ACE files from Python.

## Installation

```
$ pip install garmin_ace
```

## Usage

### Decoding a ACE file to Python objects

```
from garmin_ace import ACEFileDecoder

checklists_obj = ACEFileDecoder.read_from_file('checklist.ace')
```

See `models.py` for the data structure.

### Encoding a ACE file from Python objects

```
from garmin_ace import ACEFileEncoder

ACEFileEncoder(checklists_obj).write_to_file('checklist2.ace')
```

## Running tests (source)

```
$ make test
$ make coverage
```

## Credits

Originally based on the Swift implementation https://github.com/RISCfuture/GarminACE

## License

Copyright (C) 2023  Xavier Antoviaque

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


