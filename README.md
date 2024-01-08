# CPE 2.3 parser

A simple, no frills CPE 2.3 parser written in Python 3.

## Features

- Convert [CPE 2.3](https://cpe.mitre.org/specification/) IDs into Well-Formed Names (WFNs) represented using [dataclasses](https://github.com/python/cpython/blob/main/Lib/dataclasses.py).

## Usage

### Command line

To decompose one or more CPE 2.3 IDs into WFNs pass a space separated list of CPE 2.3 IDs:

```bash
poetry run cpe 'cpe:2.3:o:microsoft:windows_10_1607:10.0.14393.5427:*:*:*:*:*:arm64:*' 'cpe:2.3:a:microsoft:internet_explorer:4.0.1:sp1:*:*:*:*:*:*' | jq
```

```json
{
  "id": "cpe:2.3:o:microsoft:windows_10_1607:10.0.14393.5427:*:*:*:*:*:arm64:*",
  "part": "o",
  "vendor": "microsoft",
  "product": "windows_10_1607",
  "version": "10.0.14393.5427",
  "update": "*",
  "edition": "*",
  "language": "*",
  "sw_edition": "*",
  "target_sw": "*",
  "target_hw": "arm64",
  "other": "*"
}
{
  "id": "cpe:2.3:a:microsoft:internet_explorer:4.0.1:sp1:*:*:*:*:*:*",
  "part": "a",
  "vendor": "microsoft",
  "product": "internet_explorer",
  "version": "4.0.1",
  "update": "sp1",
  "edition": "*",
  "language": "*",
  "sw_edition": "*",
  "target_sw": "*",
  "target_hw": "*",
  "other": "*"
}
```

> ℹ️ CPE IDs should be quoted to prevent shell expansion - if you don't quote the CPE IDs, your shell will treat them as [globs](https://en.wikipedia.org/wiki/Glob_(programming)) by default.
