from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class Settings(SemanthaModelEntity):
	""" author semantha, this is a generated class do not change manually! """
	similarity_model_id: Optional[str]
	smart_cluster_similarity_model_id: Optional[str]
	keep_numbers: Optional[bool]
	min_tokens: Optional[int]
	similarity_measure: Optional[str]
	context_weight: Optional[float]
	enable_string_comparison: Optional[bool]
	default_document_type: Optional[str]
	enable_paragraph_sorting: Optional[bool]
	enable_paragraph_end_detection: Optional[bool]
	enable_boost_word_filtering_for_input_documents: Optional[bool]
	tagging_similarity_mode: Optional[str]
	enable_updating_fingerprints_on_tag_updates: Optional[bool]
	enable_paragraph_merging_based_on_formatting: Optional[bool]
	use_creation_date_from_input_document: Optional[bool]
	enable_saturated_match_colors: Optional[bool]
	enable_no_match_color_red: Optional[bool]
	enable_context_consideration: Optional[bool]
	enable_paragraph_resizing: Optional[bool]
	similarity_matcher: Optional[str]
	similarity_max_deviation: Optional[int]
	similarity_threshold: Optional[float]
	enable_tagging: Optional[bool]
	tagging_threshold: Optional[float]
	tagging_strategy: Optional[str]
	extraction_threshold: Optional[float]
	extraction_strategy: Optional[str]
	resize_paragraphs_on_extraction: Optional[bool]
	relevant_page_count: Optional[int]
	
	
SettingsSchema = class_schema(Settings, base_schema=SemanthaSchema)
