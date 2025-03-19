import inspect
from typing import get_origin, Union, get_args, Optional

from fastapi import Form, File, UploadFile
from pydantic_core import PydanticUndefined

pydantic_attributes = [
    "default",
    "default_factory",
    "alias",
    "title",
    "description",
    "const",
    "gt",
    "ge",
    "lt",
    "le",
    "min_length",
    "max_length",
    "regex",
    "multiple_of",
    "min_items",
    "max_items",
    "unique_items",
    "example",
    "deprecated",
    "exclude",
    'pattern'
]


def as_form(cls):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        field_type = model_field.annotation
        type_args = get_args(field_type)
        is_optional = get_origin(field_type) is Union and type(None) in type_args

        form_args = {}
        for item in model_field.metadata:
            for attr in pydantic_attributes:
                if hasattr(item, attr):
                    form_args[attr] = getattr(item, attr)
        form_args['default'] = model_field.default

        if not (UploadFile in type_args or field_type is UploadFile):
            param = Form(**form_args)
        else:
            if model_field.default is PydanticUndefined:
                param = File(...)
            else:
                param = File(None)

        if is_optional:
            field_type = Optional[field_type]

        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.KEYWORD_ONLY,
                default=param,
                annotation=field_type,
            )
        )

    async def as_form_func(**kwargs):
        return cls(**kwargs)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig
    setattr(cls, 'as_form', as_form_func)
    return cls
