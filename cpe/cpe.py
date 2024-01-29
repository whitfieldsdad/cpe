from dataclasses import dataclass
import dataclasses
import argparse
import fnmatch
import json
import re
import sys
from typing import Any, Iterable, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

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

        if self.vendors and not str_matches_any(cpe_id.vendor, self.vendors):
            return False
        if self.products and not str_matches_any(cpe_id.product, self.products):
            return False
        if self.is_application is not None and self.is_application != cpe_id.is_application():
            return False
        if self.is_hardware is not None and self.is_hardware != cpe_id.is_hardware():
            return False
        if self.is_operating_system is not None and self.is_operating_system != cpe_id.is_operating_system():
            return False
        return True

    def matches_any(self, cpe_ids: Iterable[Union[str, CPE]]) -> bool:
        return any(self.matches(cpe_id) for cpe_id in cpe_ids)
    
    def __call__(self, cpe_id: Union[str, CPE]) -> Any:
        return self.matches(cpe_id)


def filter_cpe_ids(cpe_ids: Iterable[CPE], search: Union[dict, Filter]) -> Iterable[CPE]:
    if isinstance(search, dict):
        search = Filter(**search)
    yield from filter(search.matches, cpe_ids)


def parse(value: str) -> CPE:
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
    parts = value.split(':') if value.count(':') == 12 else _RE_SPLIT.split(value)
    if len(parts) != 13:
        raise ValueError(f'Invalid CPE: {value}')

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
    d['id'] = value
    return CPE(**d)


def str_matches_any(value: str, patterns: Iterable[str], case_sensitive: bool = False) -> bool:
    value = value if case_sensitive else value.lower()
    for pattern in patterns:
        pattern = pattern if case_sensitive else pattern.lower()
        if str_matches(value, pattern, case_sensitive=True):
            return True
    return False


def str_matches(value: str, pattern: str, case_sensitive: bool = False) -> bool:
    if not case_sensitive:
        value = value.lower()
        pattern = pattern.lower()

    if '*' in pattern:
        return fnmatch.fnmatch(value, pattern)
    else:
        return value == pattern


def _cli():
    parser = argparse.ArgumentParser(description='CPE 2.3 parser')
    parser.add_argument('cpe-ids', nargs='*', help='CPEs to parse')
    kwargs = vars(parser.parse_args()) 
    
    if kwargs['cpe-ids']:
        cpe_ids = _split_strings_on_space_and_comma(kwargs['cpe-ids'])
        if not cpe_ids:
            logger.error("No CPE IDs parsed")
            sys.exit(1)            

    elif _stdin_is_empty:
        logger.error("A set of space/comma delimited CPE IDs is required")
        sys.exit(1)
    else:
        cpe_ids = _split_strings_on_space_and_comma(sys.stdin.readlines())
        sys.exit(1)
    
    _print_cpe_ids_as_cpes(cpe_ids)


def _split_strings_on_space_and_comma(values: Iterable[str]) -> Iterable[str]:
    result = []
    for v in values:
        v = v.strip() 
        if ',' in v:
            for s in v.split(','):
                s = s.strip()
                result.append(s)
        else:
            result.append(v)
    return result


def _print_cpe_ids_as_cpes(cpe_ids: Iterable[str]):
    for cpe_id in cpe_ids:
        try:
            cpe = parse(cpe_id)
        except ValueError as e:
            logger.warning("Failed to parse CPE ID: `%s` - %s", cpe_id, e)
        else:
            print(json.dumps(dataclasses.asdict(cpe)))


def _stdin_is_empty() -> bool:
    try:
        return sys.stdin.isatty()
    except AttributeError:
        return False


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    _cli()
