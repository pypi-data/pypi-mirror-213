"""Code generated by Speakeasy (https://speakeasyapi.dev). DO NOT EDIT."""

from __future__ import annotations
import dataclasses
import dateutil.parser
from dataclasses_json import Undefined, dataclass_json
from datetime import datetime
from marshmallow import fields
from speakeasy import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class VersionMetadataInput:
    r"""A set of keys and associated values, attached to a particular version of an Api."""
    
    meta_key: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('meta_key') }})
    r"""The key for this metadata."""
    meta_value: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('meta_value') }})
    r"""One of the values for this metadata."""
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class VersionMetadata:
    r"""A set of keys and associated values, attached to a particular version of an Api."""
    
    api_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('api_id') }})
    r"""The ID of the Api this Metadata belongs to."""
    created_at: datetime = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('created_at'), 'encoder': utils.datetimeisoformat(False), 'decoder': dateutil.parser.isoparse, 'mm_field': fields.DateTime(format='iso') }})
    r"""Creation timestamp."""
    meta_key: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('meta_key') }})
    r"""The key for this metadata."""
    meta_value: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('meta_value') }})
    r"""One of the values for this metadata."""
    version_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('version_id') }})
    r"""The version ID of the Api this Metadata belongs to."""
    workspace_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('workspace_id') }})
    r"""The workspace ID this Metadata belongs to."""
    