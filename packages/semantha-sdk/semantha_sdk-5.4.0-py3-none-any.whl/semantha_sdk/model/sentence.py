from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.document_named_entity import DocumentNamedEntity
from semantha_sdk.model.rect import Rect
from semantha_sdk.model.reference import Reference
from typing import List, Optional


@dataclass(frozen=True)
class Sentence(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	text: Optional[str]
	document_name: Optional[str]
	named_entities: Optional[List[DocumentNamedEntity]]
	references: Optional[List[Reference]]
	areas: Optional[List[Rect]]
	
	
SentenceSchema = class_schema(Sentence, base_schema=SemanthaSchema)
