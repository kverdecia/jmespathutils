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

    @jmespath.functions.signature({'types': ['array']}, {'types': ['expref']})
    def _func_unique_by(self, array: list[Any], expref: Any) -> Any:
        if not array:
            return array
        key_func = self._create_key_func(expref, ['number', 'string'], 'unique_by')  # type: ignore
        added = set()
        result = []
        for item in array:
            key = key_func(item)
            if key not in added:
                added.add(key)
                result.append(item)
        return result

    @jmespath.functions.signature({'types': ['array']}, {'types': ['string']})
    def _func_to_object(self, array: list[Any], key_name: str) -> list[Any]:
        """Returns an array of new objects. Each object in the result has a single key. The name
        of the key is the value of the `key_name` parameter. The value of the key is the value
        of the corresponding item in the `array` parameter.

        Args:
            array (list[Any]): The list of values to convert to objects.
            key_name (str): Name of the key of the new objects.

        Returns:
            list[Any]: The list of new objects.
        """
        return [{key_name: item} for item in array]


class ContextFunctions(Functions):
    _context: dict[str, Any]

    def __init__(self, context: dict[str, Any], *args, **kwargs):
        self._context = context
        super().__init__(*args, **kwargs)

    @jmespath.functions.signature()
    def _func_context(self) -> dict[str, Any] | None:
        return self._context
