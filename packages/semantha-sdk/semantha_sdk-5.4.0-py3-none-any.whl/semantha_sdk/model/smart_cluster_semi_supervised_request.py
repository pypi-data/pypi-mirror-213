from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.semi_super_vised_document import SemiSuperVisedDocument
from typing import List, Optional


@dataclass(frozen=True)
class SmartClusterSemiSupervisedRequest(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	clustering_name: Optional[str]
	min_cluster_size: Optional[str]
	clustering_structure: Optional[str]
	topic_over_time_range: Optional[str]
	reduce_outliers: Optional[bool]
	umap_nr_of_neighbors: Optional[int]
	documents: Optional[List[SemiSuperVisedDocument]]
	
	
SmartClusterSemiSupervisedRequestSchema = class_schema(SmartClusterSemiSupervisedRequest, base_schema=SemanthaSchema)
