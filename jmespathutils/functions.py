from typing import Any
import uuid

import cuid
import jmespath
import jmespath.functions
import jmespath.exceptions
import xmltodict


class Functions(jmespath.functions.Functions):
    @jmespath.functions.signature({'types': ['string', 'null']})
    def _func_xml_to_json(self, xml: str) -> Any:
        if xml is None:
            return None
        return xmltodict.parse(xml)

    @jmespath.functions.signature()
    def _func_uuid(self) -> str:
        return str(uuid.uuid4())

    @jmespath.functions.signature()
    def _func_cuid(self) -> str:
        return cuid.cuid()

    @jmespath.functions.signature({"types": ['array-string', 'array-number']})
    def _func_unique(self, items: list[str | int | float]) -> Any:
        return list(frozenset(items))


class ContextFunctions(Functions):
    _context: dict[str, Any]

    def __init__(self, context: dict[str, Any], *args, **kwargs):
        self._context = context
        super().__init__(*args, **kwargs)

    @jmespath.functions.signature()
    def _func_context(self) -> dict[str, Any] | None:
        return self._context
