# CPE 2.3 parser

A simple, no frills, dependency-free CPE 2.3 parser written in Python 3.

## Features

- Convert [CPE 2.3](https://cpe.mitre.org/specification/) IDs into Well-Formed Names (WFNs) represented using [dataclasses](https://github.com/python/cpython/blob/main/Lib/dataclasses.py).

> ℹ️ A GZIP compressed JSONL file containing information about every CPE 2.3 ID in the NVD is available in `data/cpes.jsonl.gz` and has the following format:

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

## Usage

### Command line

To use a local copy of the script:

```bash
python3 cpe.py 
```

To use a remote copy of the script:

```bash
curl https://gist.githubusercontent.com/whitfieldsdad/0b0db7da70b13a892c58e9b5acf0a7ec/raw/885d648f29d1d8240df2f374c3ea7a7fa553c65a/cpe.py | python3 - 'cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*'
```

Example output:

```json
{"id": "cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*", "part": "a", "vendor": "microsoft", "product": "sql_server", "version": "-", "update": "*", "edition": "*", "language": "*", "sw_edition": "*", "target_sw": "*", "target_hw": "*", "other": "*"}
```

> ℹ️ CPE IDs can be passed positionally or via stdin
 
> ℹ️ CPE IDs should be quoted to prevent shell expansion - if you don't quote the CPE IDs, your shell will treat them as [globs](https://en.wikipedia.org/wiki/Glob_(programming)) by default.

#### Parsing every CPE 2.3 ID in the NVD

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
