from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class ParagraphUpdate(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	text: Optional[str]
	type: Optional[str]
	
	
ParagraphUpdateSchema = class_schema(ParagraphUpdate, base_schema=SemanthaSchema)
