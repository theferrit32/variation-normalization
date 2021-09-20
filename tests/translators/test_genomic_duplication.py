"""Module for testing Genomic Duplication Translator."""
import unittest
from variation.classifiers import GenomicDuplicationClassifier
from variation.translators import GenomicDuplication
from variation.validators import GenomicDuplication as GD_V
from .translator_base import TranslatorBase
from variation.tokenizers import GeneSymbol
from variation.data_sources import TranscriptMappings, SeqRepoAccess, \
    MANETranscriptMappings, UTA
from variation.mane_transcript import MANETranscript
from ga4gh.vrs.dataproxy import SeqRepoDataProxy
from ga4gh.vrs.extras.translator import Translator
from gene.query import QueryHandler as GeneQueryHandler


class TestGenomicDuplicationTranslator(TranslatorBase, unittest.TestCase):
    """A class to test the Genomic Duplication Translator."""

    def classifier_instance(self):
        """Return genomic duplication instance."""
        return GenomicDuplicationClassifier()

    def validator_instance(self):
        """Return genomic duplication instance."""
        seqrepo_access = SeqRepoAccess()
        transcript_mappings = TranscriptMappings()
        uta = UTA()
        dp = SeqRepoDataProxy(seqrepo_access.seq_repo_client)
        tlr = Translator(data_proxy=dp)
        return GD_V(
            seqrepo_access, transcript_mappings,
            GeneSymbol(GeneQueryHandler()),
            MANETranscript(seqrepo_access, transcript_mappings,
                           MANETranscriptMappings(), uta),
            uta, dp, tlr
        )

    def translator_instance(self):
        """Return genomic duplication instance."""
        return GenomicDuplication()

    def fixture_name(self):
        """Return the fixture name for genomic duplication."""
        return 'genomic_duplication'
