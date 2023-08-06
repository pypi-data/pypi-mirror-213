from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.distance import Distance
from typing import Optional


@dataclass(frozen=True)
class Features(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	distance: Optional[Distance]
	font_size: Optional[int]
	bold: Optional[bool]
	italic: Optional[bool]
	page: Optional[int]
	page_rev: Optional[int]
	page_width: Optional[float]
	page_aspect_ratio: Optional[float]
	uppercase: Optional[bool]
	starts_with: Optional[str]
	contains_text: Optional[bool]
	language: Optional[str]
	relative_fontsize: Optional[str]
	
	
FeaturesSchema = class_schema(Features, base_schema=SemanthaSchema)
