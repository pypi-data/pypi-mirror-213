from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.instance_child import InstanceChild
from semantha_sdk.model.simple_property import SimpleProperty
from typing import List, Optional


@dataclass(frozen=True)
class Instance(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	class_id: str
	relation_id: Optional[str]
	type: Optional[str]
	ignore_import: Optional[bool]
	simple_properties: Optional[List[SimpleProperty]]
	comment: Optional[str]
	instances: Optional[List["Instance"]]
	childs: Optional[List[InstanceChild]]
	
	
InstanceSchema = class_schema(Instance, base_schema=SemanthaSchema)
