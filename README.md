# CPE 2.3 parser

A simple, no frills, dependency-free CPE 2.3 parser written in Python 3.

## Features

- Convert [CPE 2.3](https://cpe.mitre.org/specification/) IDs into Well-Formed Names (WFNs) represented using [dataclasses](https://github.com/python/cpython/blob/main/Lib/dataclasses.py).

## Usage

### Command line

### Parsing CPE 2.3 IDs on the command line

To parse one or more CPE IDs on the command line, provide a space delimited list of CPE IDs:

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

### Parsing every CPE 2.3 ID in the NVD

`data/cpe.txt.gz` is a GZIP compressed text file containing every CPE 2.3 ID in the [NVD](https://nvd.nist.gov/). 

To parse every CPE ID in the NVD, use `gzcat` to decompress the file, pipe it to `python3`, and pipe the output to `jq`:

```bash
gzcat data/cpes.txt.gz | python3 cpe/cpe.py | jq
```

```json
...
{
  "id": "cpe:2.3:o:microsoft:windows_server_2022_23h2:10.0.25398.521:*:*:*:*:*:x64:*",
  "part": "o",
  "vendor": "microsoft",
  "product": "windows_server_2022_23h2",
  "version": "10.0.25398.521",
  "update": "*",
  "edition": "*",
  "language": "*",
  "sw_edition": "*",
  "target_sw": "*",
  "target_hw": "x64",
  "other": "*"
}
{
  "id": "cpe:2.3:o:microsoft:windows_server_2022_23h2:10.0.25398.531:*:*:*:*:*:x64:*",
  "part": "o",
  "vendor": "microsoft",
  "product": "windows_server_2022_23h2",
  "version": "10.0.25398.531",
  "update": "*",
  "edition": "*",
  "language": "*",
  "sw_edition": "*",
  "target_sw": "*",
  "target_hw": "x64",
  "other": "*"
}
...
```

If you'd prefer JSONL output:

```bash
gzcat data/cpes.txt.gz | python3 cpe/cpe.py | jq -c
```

```json
...
{"id":"cpe:2.3:o:microsoft:windows_server_2022_23h2:10.0.25398.521:*:*:*:*:*:x64:*","part":"o","vendor":"microsoft","product":"windows_server_2022_23h2","version":"10.0.25398.521","update":"*","edition":"*","language":"*","sw_edition":"*","target_sw":"*","target_hw":"x64","other":"*"}
{"id":"cpe:2.3:o:microsoft:windows_server_2022_23h2:10.0.25398.531:*:*:*:*:*:x64:*","part":"o","vendor":"microsoft","product":"windows_server_2022_23h2","version":"10.0.25398.531","update":"*","edition":"*","language":"*","sw_edition":"*","target_sw":"*","target_hw":"x64","other":"*"}
...
```

To write the results to a GZIP compressed output file:

```bash
gzcat data/cpes.txt.gz | python3 cpe/cpe.py | jq -c '.' | gzip > data/cpes.jsonl.gz
```
