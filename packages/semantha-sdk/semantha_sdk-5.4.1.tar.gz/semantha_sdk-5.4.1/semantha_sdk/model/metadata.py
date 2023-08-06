from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class Metadata(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	read_only: Optional[bool]
	type: str
	
	
MetadataSchema = class_schema(Metadata, base_schema=SemanthaSchema)
