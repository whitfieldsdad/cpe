# Scripts

## Download all CPEs from the NVD in JSONL format

To write to stdout:

```bash
./download-cpes-in-jsonl-format.sh
```

```json
...
{"id":"cpe:2.3:a:imagemagick:imagemagick:5.4.7:*:*:*:*:*:*:*","part":"a","vendor":"imagemagick","product":"imagemagick","version":"5.4.7","update":"*","edition":"*","language":"*","sw_edition":"*","target_sw":"*","target_hw":"*","other":"*"}
{"id":"cpe:2.3:a:imagemagick:imagemagick:5.4.7.4:*:*:*:*:*:*:*","part":"a","vendor":"imagemagick","product":"imagemagick","version":"5.4.7.4","update":"*","edition":"*","language":"*","sw_edition":"*","target_sw":"*","target_hw":"*","other":"*"}
{"id":"cpe:2.3:a:imagemagick:imagemagick:5.4.8:*:*:*:*:*:*:*","part":"a","vendor":"imagemagick","product":"imagemagick","version":"5.4.8","update":"*","edition":"*","language":"*","sw_edition":"*","target_sw":"*","target_hw":"*","other":"*"}
...
```

To write to a file:

```bash
./download-cpes-in-jsonl-format.sh data/cpes.jsonl
```

```bash
du -sh data/cpes.jsonl
305M    data/cpes.jsonl
```

## Download all CVEs from the NVD in plaintext format

To write to stdout:

```bash
./download-cpes-in-plaintext-format.sh
```

```json
...
cpe:2.3:a:microsoft:sql_server:-:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2000:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:6.0:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:6.5:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:7.0:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2000:gold:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2000:sp1:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2000:sp2:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2000:sp3:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2000:sp3a:*:*:*:*:*:*
...
```

To write to a file:

```bash
./download-cpes-in-plaintext-format.sh data/cpes.txt
```

```bash
du -sh data/cpes.txt
80M    data/cpes.txt
```
