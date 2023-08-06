from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import List, Optional


@dataclass(frozen=True)
class DocumentClassBulk(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	document_ids: Optional[List[str]]
	sub_classes: Optional[List["DocumentClassBulk"]]
	tags: Optional[List[str]]
	color: Optional[str]
	comment: Optional[str]
	created: Optional[int]
	updated: Optional[int]
	metata: Optional[str]
	
	
DocumentClassBulkSchema = class_schema(DocumentClassBulk, base_schema=SemanthaSchema)
