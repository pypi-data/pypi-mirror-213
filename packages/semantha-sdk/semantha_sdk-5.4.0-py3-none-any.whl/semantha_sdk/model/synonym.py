from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import List, Optional


@dataclass(frozen=True)
class Synonym(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	word: Optional[str]
	regex: Optional[str]
	synonym: Optional[str]
	tags: Optional[List[str]]
	
	
SynonymSchema = class_schema(Synonym, base_schema=SemanthaSchema)
