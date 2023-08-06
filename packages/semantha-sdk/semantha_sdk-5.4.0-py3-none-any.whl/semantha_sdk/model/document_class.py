from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.document_class_node import DocumentClassNode
from typing import List, Optional


@dataclass(frozen=True)
class DocumentClass(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	parent_id: Optional[str]
	metadata: Optional[str]
	documents_count: Optional[int]
	sub_classes: Optional[List[DocumentClassNode]]
	tags: Optional[List[str]]
	derived_tags: Optional[List[str]]
	color: Optional[str]
	derived_color: Optional[str]
	comment: Optional[str]
	derived_comment: Optional[str]
	created: Optional[int]
	updated: Optional[int]
	derived_metadata: Optional[str]
	
	
DocumentClassSchema = class_schema(DocumentClass, base_schema=SemanthaSchema)
