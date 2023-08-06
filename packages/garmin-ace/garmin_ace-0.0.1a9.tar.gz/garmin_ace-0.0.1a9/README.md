Garmin Aviation Checklist Editor (ACE) - Python Module
======================================================

Convert ACE files to/from various formats (HTML, orgmode). Parse and write ACE files from Python.

## Installation

```
$ pip install garmin_ace
```

## Usage

Display the available formats:

```
$ ace-convert
Convert source file to destination file
Usage: ace-convert <source> <dest>
Supported source formats are: .org, .ace
Supported destination formats are: .ace, .html
```

### Example: Converting an ACE file to HTML and PDF

```
$ ace-convert checklist.ace checklist.html
```

You can further convert the HTML document to a PDF file with https://wkhtmltopdf.org/downloads.html

```
$ wkhtmltopdf checklist.html checklist.pdf
```

### Example: Converting orgmode checklists to the ACE format

Org mode is a plaintext format, which can be easier to edit and manipulate than the Garmin Checklist Editor app. It expects a simple structure:

```
* Pre-flight checklist
** Master: on
** Lights: on
** Master: off
* Startup checklist
** Master: on
...
```

The top level bullet points are the checklist names, and subitems are the checklist items.

To convert it to the other available formats:

```
$ ace-convert checklist.org checklist.ace
```

or 

```
$ ace-convert checklist.org checklist.html
```

See https://orgmode.org/worg/org-syntax.html for details on the format. 

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


