from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class Distance(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	top: Optional[float]
	bottom: Optional[float]
	left: Optional[float]
	right: Optional[float]
	
	
DistanceSchema = class_schema(Distance, base_schema=SemanthaSchema)
