from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.extraction_file import ExtractionFile
from semantha_sdk.model.model_instance import ModelInstance
from semantha_sdk.model.process_information import ProcessInformation
from semantha_sdk.model.table_instance import TableInstance
from typing import List, Optional


@dataclass(frozen=True)
class SemanticModel(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	files: Optional[List[ExtractionFile]]
	instances: Optional[List[ModelInstance]]
	tables: Optional[List[TableInstance]]
	process_information: Optional[ProcessInformation]
	
	
SemanticModelSchema = class_schema(SemanticModel, base_schema=SemanthaSchema)
