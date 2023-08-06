from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.annotation_cell import AnnotationCell
from typing import List, Optional


@dataclass(frozen=True)
class AnnotationPage(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	height: Optional[int]
	width: Optional[int]
	page_number: Optional[int]
	ignore_page: Optional[bool]
	cells: Optional[List[AnnotationCell]]
	
	
AnnotationPageSchema = class_schema(AnnotationPage, base_schema=SemanthaSchema)
