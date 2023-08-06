from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.complex_property import ComplexProperty
from semantha_sdk.model.extraction_reference import ExtractionReference
from semantha_sdk.model.file_reference import FileReference
from semantha_sdk.model.finding import Finding
from semantha_sdk.model.label import Label
from semantha_sdk.model.linked_instance import LinkedInstance
from semantha_sdk.model.metadata import Metadata
from semantha_sdk.model.simple_property import SimpleProperty
from typing import List, Optional


@dataclass(frozen=True)
class ModelInstance(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	class_id: str
	relation_id: Optional[str]
	type: Optional[str]
	ignore_import: Optional[bool]
	simple_properties: Optional[List[SimpleProperty]]
	metadata: Optional[List[Metadata]]
	qualified_name: Optional[str]
	extractor_class_ids: Optional[List[str]]
	label: Optional[str]
	labels: Optional[List[Label]]
	file: Optional[FileReference]
	complex_properties: Optional[List[ComplexProperty]]
	findings: Optional[List[Finding]]
	references: Optional[List[ExtractionReference]]
	linked_instances: Optional[List[LinkedInstance]]
	
	
ModelInstanceSchema = class_schema(ModelInstance, base_schema=SemanthaSchema)
