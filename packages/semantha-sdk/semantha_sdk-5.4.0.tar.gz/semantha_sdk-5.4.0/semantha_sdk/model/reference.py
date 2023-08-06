from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Dict, Optional


@dataclass(frozen=True)
class Reference(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	document_id: Optional[str]
	document_name: Optional[str]
	page_number: Optional[int]
	paragraph_id: Optional[str]
	sentence_id: Optional[str]
	similarity: Optional[float]
	text: Optional[str]
	context: Optional[Dict[str, str]]
	type: Optional[str]
	color: Optional[str]
	comment: Optional[str]
	has_opposite_meaning: Optional[bool]
	
	
ReferenceSchema = class_schema(Reference, base_schema=SemanthaSchema)
