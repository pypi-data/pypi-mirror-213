"""Code generated by Speakeasy (https://speakeasyapi.dev). DO NOT EDIT."""

from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import boundedrequest as shared_boundedrequest
from ..shared import error as shared_error
from ..shared import filters as shared_filters
from typing import Optional


@dataclasses.dataclass
class QueryEventLogRequest:
    
    filters: Optional[shared_filters.Filters] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'filters', 'serialization': 'json' }})
    r"""The filter to apply to the query."""
    

@dataclasses.dataclass
class QueryEventLogResponse:
    
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    bounded_requests: Optional[list[shared_boundedrequest.BoundedRequest]] = dataclasses.field(default=None)
    r"""OK"""
    error: Optional[shared_error.Error] = dataclasses.field(default=None)
    r"""Default error response"""
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    