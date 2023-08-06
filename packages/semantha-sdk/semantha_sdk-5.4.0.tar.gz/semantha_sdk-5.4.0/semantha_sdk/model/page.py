from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.annotation_page import AnnotationPage
from semantha_sdk.model.document_table import DocumentTable
from semantha_sdk.model.page_content import PageContent
from semantha_sdk.model.paragraph import Paragraph
from typing import List, Optional


@dataclass(frozen=True)
class Page(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	contents: Optional[List[PageContent]]
	paragraphs: Optional[List[Paragraph]]
	tables: Optional[List[DocumentTable]]
	annotation_page: Optional[AnnotationPage]
	
	
PageSchema = class_schema(Page, base_schema=SemanthaSchema)
