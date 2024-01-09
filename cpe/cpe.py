from dataclasses import dataclass
import dataclasses
import argparse
import json
import re
import sys
from typing import Any, Iterable, List, Optional, Union
import cpe.pattern_matching as pattern_matching

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



@dataclass()
class Filter:
    vendors: List[str] = dataclasses.field(default_factory=list)
    products: List[str] = dataclasses.field(default_factory=list)
    is_application: Optional[bool] = None
    is_hardware: Optional[bool] = None
    is_operating_system: Optional[bool] = None

    def matches(self, cpe_id: Union[str, CPE]) -> bool:
        if isinstance(cpe_id, str):
            cpe_id = parse(cpe_id)

        if self.vendors and not pattern_matching.matches_any(cpe_id.vendor, self.vendors):
            return False
        if self.products and not pattern_matching.matches_any(cpe_id.product, self.products):
            return False
        if self.is_application is not None and self.is_application != cpe_id.is_application():
            return False
        if self.is_hardware is not None and self.is_hardware != cpe_id.h
            return False
        if self.is_operating_system is not None and self.is_operating_system != cpe_id.is_operating_system():
            return False
        return True

    def matches_any(self, cpe_ids: Iterable[CPE]) -> bool:
        return any(self.matches(cpe_id) for cpe_id in cpe_ids)
    
    def __call__(self, cpe_id: Union[str, CPE]) -> Any:
        return self.matches(cpe_id)


def filter_cpe_ids(cpe_ids: Iterable[CPE], search: Union[dict, Filter]) -> Iterable[CPE]:
    if isinstance(search, dict):
        search = Filter(**search)
    yield from filter(search.matches, cpe_ids)


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
    # ~99.9% of CPEs can be split on ':', and when parsing ~1.24M CPEs this is ~10% faster
    parts = cpe.split(':') if cpe.count(':') == 12 else _RE_SPLIT.split(cpe)
    if len(parts) != 13:
        raise ValueError(f'Invalid CPE: {cpe}')

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
        if _stdin_is_empty():
            parser.print_help()
            sys.exit(1)
        
        cpes = sys.stdin.read().splitlines()
    else:
        cpes = args.cpes

    for cpe in cpes:
        try:
            wfn = parse(cpe)
        except TypeError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        
        blob = json.dumps(dataclasses.asdict(wfn))
        print(blob)


def _stdin_is_empty() -> bool:
    try:
        return sys.stdin.isatty()
    except AttributeError:
        return False


if __name__ == '__main__':
    _cli()
