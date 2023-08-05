from typing import Any, Optional, Iterable


async def serializable(dictionary: dict[str, Any], exceptions: Iterable[str] = ()) -> dict[str, Any]:
    def validate(value: Any):
        if isinstance(value, bool):
            return True
        elif value is None:
            return False
        elif isinstance(value, str):
            return len(value)

    return {key: value for key, value in dictionary.items() if validate(value) or key in exceptions}


async def find(
        where: list[dict[str, Any]],
        key: Any,
        value: Any
) -> tuple[Optional[int], Optional[dict[str, Any]]]:
    for index, item in enumerate(where):
        if item.get(key) == value:
            return index, item
    return None, None
