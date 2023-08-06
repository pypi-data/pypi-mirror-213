from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.document import Document
from typing import Optional


@dataclass(frozen=True)
class ExtractionFile(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	external_id: Optional[str]
	name: Optional[str]
	processed: Optional[bool]
	binary: Optional[str]
	documentextractor: Optional[str]
	document: Optional[Document]
	filename: Optional[str]
	created: Optional[int]
	
	
ExtractionFileSchema = class_schema(ExtractionFile, base_schema=SemanthaSchema)
