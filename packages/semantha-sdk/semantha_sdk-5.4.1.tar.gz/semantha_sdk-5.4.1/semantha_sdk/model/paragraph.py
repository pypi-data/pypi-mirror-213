from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.rect import Rect
from semantha_sdk.model.reference import Reference
from semantha_sdk.model.sentence import Sentence
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Paragraph(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	text: Optional[str]
	type: Optional[str]
	id: Optional[str]
	document_name: Optional[str]
	sentences: Optional[List[Sentence]]
	references: Optional[List[Reference]]
	context: Optional[Dict[str, str]]
	areas: Optional[List[Rect]]
	comment: Optional[str]
	verified: Optional[bool]
	data_url_image: Optional[str]
	references_safe: Optional[List[Reference]]
	
	
ParagraphSchema = class_schema(Paragraph, base_schema=SemanthaSchema)
