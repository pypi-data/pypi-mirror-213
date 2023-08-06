from __future__ import annotations

import dataclasses
import inspect
import typing

import sila.server as sila

from . import utils
from .data_type_definition import DataTypeDefinition


def parse(type_hint: typing.Type, feature: sila.Feature) -> sila.data_types.DataType:
    origin = typing.get_origin(type_hint) or type_hint

    if origin is None:
        return sila.data_types.Void()
    if issubclass(origin, DataTypeDefinition):
        if data_type := next(
            iter(
                [
                    data_type_definition
                    for data_type_definition in feature.data_type_definitions
                    if data_type_definition.identifier == origin.identifier
                ]
            ),
            None,
        ):
            return data_type

        docs = utils.parse_docs(inspect.getdoc(origin) or "")
        fields = dataclasses.fields(origin)

        if len(fields) == 1 and utils.humanize(fields[0].name).replace(" ", "") == origin.identifier:
            data_type_definition = sila.data_types.DataTypeDefinition(
                identifier=origin.identifier,
                display_name=origin.display_name,
                description=origin.description,
                factory=type_hint,
                data_type=parse(fields[0].type, feature),
            )

            feature.add_data_type_definition(data_type_definition)
            return data_type_definition

        elements: list[sila.data_types.Structure.Element] = []
        for index, field in enumerate(fields):
            field_display_name = utils.humanize(field.name)
            elements.append(
                sila.data_types.Structure.Element(
                    identifier=field_display_name.replace(" ", ""),
                    display_name=field_display_name,
                    description=docs.get("parameter", [])[index].get("default", ""),
                    data_type=parse(field.type, feature),
                )
            )

        data_type_definition = sila.data_types.DataTypeDefinition(
            identifier=origin.identifier,
            display_name=origin.display_name,
            description=origin.description,
            factory=lambda x: type_hint(*x.values()),
            data_type=sila.data_types.Structure(elements=elements),
        )
        feature.add_data_type_definition(data_type_definition)
        return data_type_definition
    if issubclass(origin, sila.data_types.DataType):
        return origin()
    if issubclass(origin, bool):
        return sila.data_types.Boolean()
    if issubclass(origin, int):
        return sila.data_types.Integer()
    if issubclass(origin, float):
        return sila.data_types.Real()
    if issubclass(origin, str):
        return sila.data_types.String()
    if issubclass(origin, bytes):
        return sila.data_types.Binary()
    if issubclass(origin, sila.datetime.date):
        return sila.data_types.Date()
    if issubclass(origin, sila.datetime.time):
        return sila.data_types.Time()
    if issubclass(origin, sila.datetime.datetime):
        return sila.data_types.Timestamp()
    if issubclass(origin, list):
        arg = typing.get_args(type_hint)[0]
        return sila.data_types.List(data_type=parse(arg, feature))
    if issubclass(origin, typing.Annotated):
        args = typing.get_args(type_hint)
        return sila.data_types.Constrained(data_type=parse(args[0], feature), constraints=list(args[1:]))

    return sila.data_types.Void()
