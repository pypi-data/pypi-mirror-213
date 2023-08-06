from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.extraction_area import ExtractionArea
from semantha_sdk.model.extraction_reference import ExtractionReference
from semantha_sdk.model.finding import Finding
from semantha_sdk.model.label import Label
from semantha_sdk.model.metadata import Metadata
from typing import List, Optional


@dataclass(frozen=True)
class ComplexProperty(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	name: str
	value: str
	label: Optional[str]
	id: Optional[str]
	class_id: Optional[str]
	relation_id: Optional[str]
	original_value: Optional[str]
	extracted_value: Optional[str]
	datatype: Optional[str]
	labels: Optional[List[Label]]
	metadata: Optional[List[Metadata]]
	extraction_area: Optional[ExtractionArea]
	findings: Optional[List[Finding]]
	references: Optional[List[ExtractionReference]]
	
	
ComplexPropertySchema = class_schema(ComplexProperty, base_schema=SemanthaSchema)
