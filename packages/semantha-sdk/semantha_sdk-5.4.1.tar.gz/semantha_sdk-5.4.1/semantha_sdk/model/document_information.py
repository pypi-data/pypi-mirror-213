from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.entity import Entity
from typing import List, Optional


@dataclass(frozen=True)
class DocumentInformation(SemanthaModelEntity):
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
	document_class_id: Optional[str]
	
	
DocumentInformationSchema = class_schema(DocumentInformation, base_schema=SemanthaSchema)
