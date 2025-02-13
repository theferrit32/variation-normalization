"""A module for Coding DNA Deletion Tokenization."""
from typing import Dict, Optional

from variation.schemas.token_response_schema import CodingDNADeletionToken
from variation.tokenizers.deletion_base import DeletionBase


class CodingDNADeletion(DeletionBase):
    """Class for tokenizing Deletion at the coding dna reference sequence."""

    def return_token(self, params: Dict) -> Optional[CodingDNADeletionToken]:
        """Return coding DNA Deletion token if match

        :param Dict params: Matched parameters for deletion
        :return: `CodingDNADeletionToken` if on c coordinate, else `None`
        """
        if params["coordinate_type"] == "c":
            return CodingDNADeletionToken(**params)
