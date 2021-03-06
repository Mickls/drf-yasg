import uuid

import pytest

from drf_yasg import openapi
from drf_yasg.inspectors.field import get_basic_type_info_from_hint

try:
    import typing
    from typing import Dict, List, Union, Optional, Set
except ImportError:
    typing = None

if typing:
    @pytest.mark.parametrize('hint_class, expected_swagger_type_info', [
        (int, {'type': openapi.TYPE_INTEGER, 'format': None}),
        (str, {'type': openapi.TYPE_STRING, 'format': None}),
        (bool, {'type': openapi.TYPE_BOOLEAN, 'format': None}),
        (dict, {'type': openapi.TYPE_OBJECT, 'format': None}),
        (Dict[int, int], {'type': openapi.TYPE_OBJECT, 'format': None}),
        (uuid.UUID, {'type': openapi.TYPE_STRING, 'format': openapi.FORMAT_UUID}),
        (List[int], {'type': openapi.TYPE_ARRAY, 'items': openapi.Items(openapi.TYPE_INTEGER)}),
        (List[str], {'type': openapi.TYPE_ARRAY, 'items': openapi.Items(openapi.TYPE_STRING)}),
        (List[bool], {'type': openapi.TYPE_ARRAY, 'items': openapi.Items(openapi.TYPE_BOOLEAN)}),
        (Set[int], {'type': openapi.TYPE_ARRAY, 'items': openapi.Items(openapi.TYPE_INTEGER)}),
        (Optional[bool], {'type': openapi.TYPE_BOOLEAN, 'format': None, 'x-nullable': True}),
        (Optional[List[int]], {
            'type': openapi.TYPE_ARRAY, 'items': openapi.Items(openapi.TYPE_INTEGER), 'x-nullable': True
        }),
        (Union[List[int], type(None)], {
            'type': openapi.TYPE_ARRAY, 'items': openapi.Items(openapi.TYPE_INTEGER), 'x-nullable': True
        }),
        # Following cases are not 100% correct, but it should work somehow and not crash.
        (Union[int, float], None),
        (List, {'type': openapi.TYPE_ARRAY, 'items': openapi.Items(openapi.TYPE_STRING)}),
        ('SomeType', None),
        (type('SomeType', (object,), {}), None),
        (None, None),
        (6, None),
    ])
    def test_get_basic_type_info_from_hint(hint_class, expected_swagger_type_info):
        type_info = get_basic_type_info_from_hint(hint_class)
        assert type_info == expected_swagger_type_info
