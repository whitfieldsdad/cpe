from dataclasses import dataclass
import dataclasses
import argparse
import json
import re
import sys

_RE_SPLIT = re.compile(r'(?<!\\):')


@dataclass()
class CPE:
    id: str
    part: str
    vendor: str
    product: str
    version: str
    update: str
    edition: str
    language: str
    sw_edition: str
    target_sw: str
    target_hw: str
    other: str

    def is_application(self) -> bool:
        return self.part == 'a'
    
    def is_hardware(self) -> bool:
        return self.part == 'h'
    
    def is_operating_system(self) -> bool:
        return self.part == 'o'


def parse(cpe: str) -> CPE:
    """
    Decompose a CPE string into a Well Formed Name (WFN).

    Example CPEs:

    - cpe:2.3:o:microsoft:windows_10_1607:10.0.14393.5427:*:*:*:*:*:arm64:*
    - cpe:2.3:a:microsoft:internet_explorer:4.0.1:sp1:*:*:*:*:*:*
    - cpe:2.3:a:microsoft:remote_desktop:1.2.605:*:*:*:*:windows:*:*
    - cpe:2.3:o:microsoft:windows_nt:4.0:sp5:*:*:embedded:*:x86:*
    - cpe:2.3:a:zoom:zoom_plugin_for_microsoft_outlook:4.8.20547.0412:*:*:*:*:macos:*:*

    Example decomposition:

    >>> import cpe
    >>> result = cpe.parse('cpe:2.3:o:microsoft:windows_10_1607:10.0.14393.5427:*:*:*:*:*:arm64:*')
    >>> print(result)
    CPE(id='cpe:2.3:o:microsoft:windows_10_1607:10.0.14393.5427:*:*:*:*:*:arm64:*', part='o', vendor='microsoft', product='windows_10_1607', version='10.0.14393.5427', update='*', edition='*', language='*', sw_edition='*', target_sw='*', target_hw='arm64', other='*')

    >>> import dataclasses
    >>> import json
    >>> print(json.dumps(dataclasses.asdict(result), indent=2))
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
    """
    parts = _RE_SPLIT.split(cpe)
    if len(parts) != 13:
        raise TypeError(f'Invalid CPE: {cpe}')

    prefix, version = parts.pop(0), parts.pop(0)
    if prefix != 'cpe':
        raise ValueError(f'Invalid CPE prefix: {prefix}')
    elif version != '2.3':
        raise ValueError(f'Unsupported CPE version: {version}')
    
    keys = [
        'part',
        'vendor',
        'product',
        'version',
        'update',
        'edition',
        'language',
        'sw_edition',
        'target_sw',
        'target_hw',
        'other',
    ]
    d = dict(zip(keys, parts))
    d['id'] = cpe
    return CPE(**d)


def _cli():
    parser = argparse.ArgumentParser(description='CPE 2.3 parser')
    parser.add_argument('cpes', nargs='*', help='CPEs to parse')
    args = parser.parse_args()
    if not args.cpes:
        cpes = sys.stdin.read().splitlines()
    else:
        cpes = args.cpes

    for cpe in cpes:
        wfn = parse(cpe)
        blob = json.dumps(dataclasses.asdict(wfn))
        print(blob)


if __name__ == '__main__':
    _cli()
