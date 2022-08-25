"""Module containing schemas used in HGVS To Copy Number endpoints"""
from typing import Optional, Type, Any, Dict, Union

from ga4gh.vrsatile.pydantic.vrs_models import RelativeCopyClass, AbsoluteCopyNumber, \
    RelativeCopyNumber, Text
from pydantic import StrictStr

from variation.schemas.classification_response_schema import ClassificationType
from variation.schemas.normalize_response_schema import ServiceResponse


VALID_CLASSIFICATION_TYPES = [
    ClassificationType.GENOMIC_DUPLICATION,
    ClassificationType.GENOMIC_DELETION,
    ClassificationType.GENOMIC_DELETION_RANGE,
    ClassificationType.GENOMIC_UNCERTAIN_DELETION
]

VALID_RELATIVE_COPY_CLASS = [rcc.value for
                             rcc in RelativeCopyClass.__members__.values()]


class HgvsToAbsoluteCopyNumberService(ServiceResponse):
    """A response for translating HGVS to absolute copy number."""

    hgvs_expr: StrictStr
    absolute_copy_number: Optional[Union[AbsoluteCopyNumber, Text]]

    class Config:
        """Configure model."""

        @staticmethod
        def schema_extra(schema: Dict[str, Any],
                         model: Type["HgvsToAbsoluteCopyNumberService"]) -> None:
            """Configure OpenAPI schema."""
            if "title" in schema.keys():
                schema.pop("title", None)
            for prop in schema.get("properties", {}).values():
                prop.pop("title", None)
            schema["example"] = {
                "hgvs_expr": "NC_000003.12:g.49531262dup",
                "absolute_copy_number": {
                    "id": "ga4gh:ACN._C6yp4SRGVfuRmMiJShIKYCK3dSX0vNF",
                    "type": "AbsoluteCopyNumber",
                    "location": {
                        "id": "ga4gh:SL.KefUQwlqEBGtzoNO-MzOozx7_H1uP-fD",
                        "type": "SequenceLocation",
                        "sequence_id": "ga4gh:SQ.Zu7h9AggXxhTaGVsy7h_EZSChSZGcmgX",
                        "start": {"type": "Number", "value": 49531260},
                        "end": {"type": "Number", "value": 49531262}
                    },
                    "copies": {"type": "Number", "value": 3}
                },
                "service_meta_": {
                    "name": "variation-normalizer",
                    "version": "0.2.17",
                    "response_datetime": "2022-01-26T22:23:41.821673",
                    "url": "https://github.com/cancervariants/variation-normalization"
                }
            }


class HgvsToRelativeCopyNumberService(ServiceResponse):
    """A response for translating HGVS to relative copy number."""

    hgvs_expr: StrictStr
    relative_copy_number: Optional[Union[RelativeCopyNumber, Text]]

    class Config:
        """Configure model."""

        @staticmethod
        def schema_extra(schema: Dict[str, Any],
                         model: Type["HgvsToRelativeCopyNumberService"]) -> None:
            """Configure OpenAPI schema."""
            if "title" in schema.keys():
                schema.pop("title", None)
            for prop in schema.get("properties", {}).values():
                prop.pop("title", None)
            schema["example"] = {
                "hgvs_expr": "NC_000003.12:g.49531262dup",
                "relative_copy_number": {
                    "id": "ga4gh:RCN._1Nz0yj2g9Q6cRO8j6oRi5peUJYjTAga",
                    "type": "RelativeCopyNumber",
                    "location": {
                        "id": "ga4gh:SL.KefUQwlqEBGtzoNO-MzOozx7_H1uP-fD",
                        "type": "SequenceLocation",
                        "sequence_id": "ga4gh:SQ.Zu7h9AggXxhTaGVsy7h_EZSChSZGcmgX",
                        "start": {"type": "Number", "value": 49531260},
                        "end": {"type": "Number", "value": 49531262}
                    },
                    "relative_copy_class": "complete loss"
                },
                "service_meta_": {
                    "name": "variation-normalizer",
                    "version": "0.2.17",
                    "response_datetime": "2022-01-26T22:23:41.821673",
                    "url": "https://github.com/cancervariants/variation-normalization"
                }
            }