"""Module for testing amino acid delins Translator."""
import unittest
from variation.classifiers import AminoAcidDelInsClassifier
from variation.translators import AminoAcidDelIns
from variation.validators import AminoAcidDelIns as AAD_V
from .translator_base import TranslatorBase
from variation.tokenizers import GeneSymbol
from variation.tokenizers.caches import GeneSymbolCache, AminoAcidCache
from variation.data_sources import TranscriptMappings, SeqRepoAccess, \
    MANETranscriptMappings, UTA
from variation.mane_transcript import MANETranscript


class TestAminoAcidDelInsTranslator(TranslatorBase, unittest.TestCase):
    """A class to test the amino acid delins Translator."""

    def classifier_instance(self):
        """Return amino acid delins instance."""
        return AminoAcidDelInsClassifier()

    def validator_instance(self):
        """Return amino acid delins instance."""
        seqrepo_access = SeqRepoAccess()
        transcript_mappings = TranscriptMappings()
        return AAD_V(
            seqrepo_access, transcript_mappings, GeneSymbol(GeneSymbolCache()),
            MANETranscript(seqrepo_access, transcript_mappings,
                           MANETranscriptMappings(), UTA()),
            AminoAcidCache())

    def translator_instance(self):
        """Return amino acid delins instance."""
        return AminoAcidDelIns()

    def fixture_name(self):
        """Return the fixture name for amino acid delins."""
        return 'amino_acid_delins'
