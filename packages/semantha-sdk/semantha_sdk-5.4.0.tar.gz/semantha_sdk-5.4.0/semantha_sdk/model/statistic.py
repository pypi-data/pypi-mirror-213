from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.tag_docs import TagDocs
from typing import List, Optional


@dataclass(frozen=True)
class Statistic(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	library_size: Optional[int]
	size: Optional[int]
	number_of_sentences: Optional[int]
	docs_per_tag: Optional[List[TagDocs]]
	
	
StatisticSchema = class_schema(Statistic, base_schema=SemanthaSchema)
