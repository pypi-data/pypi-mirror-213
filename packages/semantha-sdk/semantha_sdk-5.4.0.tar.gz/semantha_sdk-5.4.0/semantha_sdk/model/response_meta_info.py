from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.meta_info_page import MetaInfoPage
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ResponseMetaInfo(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	info: Optional[str]
	parameters: Optional[Dict[str, Any]]
	warnings: Optional[List[str]]
	page: Optional[MetaInfoPage]
	
	
ResponseMetaInfoSchema = class_schema(ResponseMetaInfo, base_schema=SemanthaSchema)
