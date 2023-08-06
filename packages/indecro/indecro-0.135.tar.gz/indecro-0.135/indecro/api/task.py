from typing import Any, Awaitable, Union, Callable

Task = Callable[..., Union[Any, Awaitable[Any]]]
