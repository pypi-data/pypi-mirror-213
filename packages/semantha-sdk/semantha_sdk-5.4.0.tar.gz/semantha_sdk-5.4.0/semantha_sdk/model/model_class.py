from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import List, Optional


@dataclass(frozen=True)
class ModelClass(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	name: Optional[str]
	label: Optional[str]
	sub_model_classes: Optional[List["ModelClass"]]
	
	
ModelClassSchema = class_schema(ModelClass, base_schema=SemanthaSchema)
