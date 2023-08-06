from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.label import Label
from semantha_sdk.model.metadata_value import MetadataValue
from typing import List, Optional


@dataclass(frozen=True)
class ClassBulk(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	read_only: Optional[bool]
	functional: Optional[bool]
	labels: Optional[List[Label]]
	metadata: Optional[List[MetadataValue]]
	comment: Optional[str]
	datatype: Optional[str]
	attribute_ids: Optional[List[str]]
	relevant_for_relation: Optional[bool]
	object_property_id: Optional[str]
	object_property_type_id: Optional[str]
	parent_id: Optional[str]
	
	
ClassBulkSchema = class_schema(ClassBulk, base_schema=SemanthaSchema)
