"""Code generated by Speakeasy (https://speakeasyapi.dev). DO NOT EDIT."""

from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from vesselapi import utils

class StringFilterMode(str, Enum):
    INSENSITIVE = 'insensitive'


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class StringFilter:
    
    contains: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('contains'), 'exclude': lambda f: f is None }})
    ends_with: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('endsWith'), 'exclude': lambda f: f is None }})
    equals: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('equals'), 'exclude': lambda f: f is None }})
    in_: Optional[list[str]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('in'), 'exclude': lambda f: f is None }})
    mode: Optional[StringFilterMode] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('mode'), 'exclude': lambda f: f is None }})
    not_: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('not'), 'exclude': lambda f: f is None }})
    not_in: Optional[list[str]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('notIn'), 'exclude': lambda f: f is None }})
    starts_with: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('startsWith'), 'exclude': lambda f: f is None }})
    