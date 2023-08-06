from typing import Type, cast

import pydantic

from mappr import types
from mappr.iterators import field_iterator


@field_iterator(test=lambda cls: issubclass(cls, pydantic.BaseModel))
def pydantic_iter_fields(model_cls: Type) -> types.FieldIterator:
    pydantic_model = cast(pydantic.BaseModel, model_cls)
    yield from pydantic_model.__fields__.keys()
