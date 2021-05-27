"""A module for testing Genomic Deletion Tokenization."""
import unittest
from variant.tokenizers import GenomicDeletion
from .tokenizer_base import TokenizerBase
from variant.tokenizers.caches import AminoAcidCache, NucleotideCache


class TestGenomicDeletionTokenizer(TokenizerBase, unittest.TestCase):
    """A class for testing Coding DNA Deletion Tokenization."""

    def tokenizer_instance(self):
        """Return Genomic Deletion instance."""
        return GenomicDeletion(AminoAcidCache(), NucleotideCache())

    def token_type(self):
        """Return genomic deletion token type."""
        return 'GenomicDeletion'

    def fixture_name(self):
        """Return the fixture name for Genomic Deletion."""
        return 'genomic_deletion'
