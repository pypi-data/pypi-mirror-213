from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.document_information import DocumentInformation
from semantha_sdk.model.response_meta_info import ResponseMetaInfo
from typing import List, Optional


@dataclass(frozen=True)
class ReferenceDocumentsResponseContainer(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	meta: Optional[ResponseMetaInfo]
	data: Optional[List[DocumentInformation]]
	
	
ReferenceDocumentsResponseContainerSchema = class_schema(ReferenceDocumentsResponseContainer, base_schema=SemanthaSchema)
