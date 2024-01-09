# CPE 2.3 parser

A simple, no frills, dependency-free CPE 2.3 parser written in Python 3.

## Features

- Decompose [CPE 2.3 IDs](https://cpe.mitre.org/specification/) into Well-Formed Names (WFNs) using [dataclasses](https://github.com/python/cpython/blob/main/Lib/dataclasses.py)
- A command line interface which produces JSONL output and accepts one or more CPE IDs positionally or via stdin

## Usage

The [script](cpe/cpe.py) is designed to be used as either a standalone tool or as a module.

- [Command line](#command-line)
  - [Parsing CPE IDs via the command line](#parsing-cpe-ids-via-the-command-line)
  - [Parsing every CPE ID in the NVD](#parsing-every-cpe-id-in-the-nvd)
- [Python](#python)
  - [Parsing CPE IDs in Python](#parsing-cpe-ids-in-python)

### Command line

#### Parsing CPE IDs via the command line

To parse one or more CPE IDs, pass in one or more CPE IDs separated by a space.

To use a local copy of the script:

```bash
python3 cpe/cpe.py 'cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*' | jq
```

To use a remote copy of the script:

```bash
curl -s https://raw.githubusercontent.com/whitfieldsdad/cpe/main/cpe/cpe.py | python3 - 'cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*' | jq
```

Example output:

```json
{
  "id": "cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*",
  "part": "a",
  "vendor": "microsoft",
  "product": "sql_server",
  "version": "-",
  "update": "*",
  "edition": "*",
  "language": "*",
  "sw_edition": "*",
  "target_sw": "*",
  "target_hw": "*",
  "other": "*"
}
```
 
> ℹ️ CPE IDs should be quoted to prevent shell expansion - if you don't quote the CPE IDs, your shell will treat them as [globs](https://en.wikipedia.org/wiki/Glob_(programming)) by default.
>
> ℹ️ CPE IDs can be passed positionally or via stdin

#### Parsing every CPE ID in the NVD

All CPE IDs in the NVD are provided in a GZIP compressed text file: `data/cpes.txt.gz`

To decompose every CPE ID into a Well Formed Name (WFN) in JSON format:

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

If you'd prefer JSONL format:

```bash
gzcat data/cpes.txt.gz | python3 cpe/cpe.py | jq -c
```

```json
...
{"id":"cpe:2.3:o:microsoft:windows_server_2022_23h2:10.0.25398.521:*:*:*:*:*:x64:*","part":"o","vendor":"microsoft","product":"windows_server_2022_23h2","version":"10.0.25398.521","update":"*","edition":"*","language":"*","sw_edition":"*","target_sw":"*","target_hw":"x64","other":"*"}
{"id":"cpe:2.3:o:microsoft:windows_server_2022_23h2:10.0.25398.531:*:*:*:*:*:x64:*","part":"o","vendor":"microsoft","product":"windows_server_2022_23h2","version":"10.0.25398.531","update":"*","edition":"*","language":"*","sw_edition":"*","target_sw":"*","target_hw":"x64","other":"*"}
...
```

To write the results to a GZIP compressed JSONL file:

```bash
gzcat data/cpes.txt.gz | python3 cpe/cpe.py | jq -c '.' | gzip > data/cpes.jsonl.gz
```

You can download all CPE IDs in JSONL format using the following command:

```bash
wget https://github.com/whitfieldsdad/cpe/raw/main/data/cpes.jsonl.gz -O - | gzcat | jq '.' -c
```

### Python

### Parsing CPE IDs in Python

To parse `cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*`:

```python
import cpe
import dataclasses
import json

result = cpe.parse('cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*')
print(json.dumps(dataclasses.asdict(result), indent=4))
```

```json
{
    "id": "cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*",
    "part": "a",
    "vendor": "microsoft",
    "product": "sql_server",
    "version": "-",
    "update": "*",
    "edition": "*",
    "language": "*",
    "sw_edition": "*",
    "target_sw": "*",
    "target_hw": "*",
    "other": "*"
}
```

### Filter CPE IDs by vendor

The `Filter` class can be used to filter CPE IDs:

```python
from cpe import Filter

cpe_id = 'cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*'
f = Filter(vendors=['microsoft'])
matches = f(cpe_id)
print(matches)
```

```text
True
```

For example, to select all CPE IDs corresponding to the Microsoft SQL Server product family:

```python
from cpe import Filter

cpe_ids = [
  'cpe:2.3:a:microsoft:sql_server_management_studio:18.6:*:*:*:*:*:*:*',
  'cpe:2.3:a:microsoft:sql_server_reporting_services:2017:*:*:*:*:*:*:*',
  'cpe:2.3:a:microsoft:sql_server_reporting_services:2019:*:*:*:*:*:*:*',
  'cpe:2.3:a:oracle:mysql_server:5.7.26:*:*:*:*:*:*:*',
  'cpe:2.3:a:oracle:mysql_server:8.0.15:*:*:*:*:*:*:*',
  'cpe:2.3:o:microsoft:sql_server:2016:sp2:*:*:*:*:x64:*',
]

f = Filter(vendors=['microsoft'], products=['*sql_server*'], is_application=True)
for cpe_id in filter(f, cpe_ids):
  print(cpe_id)
```

```text
cpe:2.3:a:microsoft:sql_server_management_studio:18.6:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server_reporting_services:2017:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server_reporting_services:2019:*:*:*:*:*:*:*
```