from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class Topic(BaseModel):
    name: str
    vocabulary: str


class TimePeriod(BaseModel):
    start: str
    end: str


class GeographicUnit(BaseModel):
    name: str
    code: str


class LicenseItem(BaseModel):
    name: str
    uri: str


class Link(BaseModel):
    type: str
    description: str
    uri: str


class ApiDocumentationItem(BaseModel):
    description: str
    uri: str


class Source(BaseModel):
    name: str


class Note(BaseModel):
    note: str


class Producer(BaseModel):
    name: str
    abbr: str
    affiliation: str
    role: str


class MetadataCreation(BaseModel):
    producers: list[Producer] | None = None
    prod_date: date | None = None
    version: str | None = None


class SeriesDescription(BaseModel):
    idno: str
    doi: str | None = None
    name: str
    database_id: str | None = None
    # aliases
    # alternate_identifiers
    measurement_unit: str | None = None
    # dimensions
    periodicity: str | None = None
    base_period: str | None = None
    definition_short: str | None = None
    definition_long: str | None = None
    # statistical_concept
    # concepts
    methodology: str | None = None
    # imputation
    # missing
    # quality_checks
    # quality_note
    # sources_discrepancies
    # series_break
    limitation: str | None = None
    # themes
    topics: list[Topic] | None = None
    # disciplines
    relevance: str | None = None
    time_periods: list[TimePeriod] | None = None
    # ref_country
    geographic_units: list[GeographicUnit] | None = None
    aggregation_method: str | None = None
    # disaggregation
    license: list[LicenseItem] | None = None
    # confidentiality
    # confidentiality_status
    links: list[Link] | None = None
    api_documentation: list[ApiDocumentationItem] | None = None
    # authoring_entity
    sources: list[Source] | None = None
    sources_note: str | None = None
    keywords: list | None = None
    # acronyms
    notes: list[Note] | None = None
    # related_indicators
    # compliance
    # framework
    # lda_topics
    # embeddings
    # series_groups


class Indicators(BaseModel):
    metadata_creation: MetadataCreation | None = None
    series_description: SeriesDescription
    schematype: str
