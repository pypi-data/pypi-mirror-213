from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.label import Label
from typing import List, Optional


@dataclass(frozen=True)
class DataProperty(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	id: Optional[str]
	name: str
	read_only: Optional[bool]
	functional: Optional[bool]
	labels: Optional[List[Label]]
	
	
DataPropertySchema = class_schema(DataProperty, base_schema=SemanthaSchema)
