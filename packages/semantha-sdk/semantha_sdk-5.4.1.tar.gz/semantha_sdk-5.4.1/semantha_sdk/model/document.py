from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.entity import Entity
from semantha_sdk.model.page import Page
from semantha_sdk.model.reference import Reference
from typing import List, Optional


@dataclass(frozen=True)
class Document(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: Optional[str]
	tags: Optional[List[str]]
	metadata: Optional[str]
	filename: Optional[str]
	created: Optional[int]
	updated: Optional[int]
	processed: Optional[bool]
	lang: Optional[str]
	content: Optional[str]
	document_class: Optional[Entity]
	derived_tags: Optional[List[str]]
	color: Optional[str]
	derived_color: Optional[str]
	comment: Optional[str]
	derived_comment: Optional[str]
	content_preview: Optional[str]
	pages: Optional[List[Page]]
	references: Optional[List[Reference]]
	image_pages: Optional[List[str]]
	document_class_id: Optional[str]
	
	
	def __hash__(self):
		return self.id
	
DocumentSchema = class_schema(Document, base_schema=SemanthaSchema)
