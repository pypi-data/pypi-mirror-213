from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class NamedEntity(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	regex: Optional[str]
	
	
NamedEntitySchema = class_schema(NamedEntity, base_schema=SemanthaSchema)
