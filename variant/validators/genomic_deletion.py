"""The module for Genomic Deletion Validation."""
from variant.validators.deletion_base import DeletionBase
from variant.schemas.classification_response_schema import \
    ClassificationType
from variant.schemas.token_response_schema import GenomicDeletionToken
from .genomic_base import GenomicBase
from typing import List
from variant.schemas.classification_response_schema import Classification
from variant.schemas.token_response_schema import GeneMatchToken
from variant.schemas.validation_response_schema import ValidationResult
from variant.schemas.token_response_schema import Token
import logging


logger = logging.getLogger('variant')
logger.setLevel(logging.DEBUG)


class GenomicDeletion(DeletionBase):
    """The Genomic Deletion Validator class."""

    def validate(self, classification: Classification) \
            -> List[ValidationResult]:
        """Validate a given classification.

        :param Classification classification: A classification for a list of
            tokens
        :return: A list of validation results
        """
        results = list()
        errors = list()

        classification_tokens = self.get_classification_tokens(classification)
        gene_tokens = self.get_gene_tokens(classification)

        if gene_tokens and len(gene_tokens) > 1:
            errors.append('More than one gene symbol found for a single'
                          f' {self.variant_name()}')

        if len(classification.non_matching_tokens) > 0:
            errors.append(f"Non matching tokens found for "
                          f"{self.variant_name()}.")

        genomic_base = GenomicBase(self.dp)
        nc_accessions = genomic_base.get_nc_accessions(classification)
        if not nc_accessions:
            errors.append('Could not find NC_ accession for '
                          f'{self.variant_name()}')

        if len(errors) > 0:
            return [self.get_validation_result(
                classification, False, 0, None,
                '', '', errors, gene_tokens)]

        self.get_valid_invalid_results(classification_tokens, nc_accessions,
                                       classification, results, gene_tokens)
        return results

    def get_hgvs_expr(self, classification, t, s, is_hgvs) -> tuple:
        """Return HGVS expression and whether or not it's an Ensembl transcript

        :param Classification classification: A classification for a list of
            tokens
        :param str t: Transcript retrieved from transcript mapping
        :param bool is_hgvs: Whether or not classification is HGVS token
        :return: A tuple containing the hgvs expression and whether or not
            it's an Ensembl Transcript
        """
        if t.startswith('ENST'):
            # TODO
            return None, True

        if not is_hgvs:
            prefix = f"{t}:{s.reference_sequence.lower()}.{s.start_pos_del}"
            if s.end_pos_del:
                prefix += f"_{s.end_pos_del}"
            hgvs_expr = f"{prefix}del"
            if s.deleted_sequence:
                hgvs_expr += f"{s.deleted_sequence}"
        else:
            hgvs_token = [t for t in classification.all_tokens if
                          isinstance(t, Token) and t.token_type == 'HGVS'][0]
            hgvs_expr = hgvs_token.input_string

        gene_token = [t for t in classification.all_tokens
                      if t.token_type == 'GeneSymbol']
        if gene_token:
            is_ensembl_transcript = True
        else:
            is_ensembl_transcript = False
        return hgvs_expr, is_ensembl_transcript

    def get_valid_invalid_results(self, classification_tokens, transcripts,
                                  classification, results, gene_tokens) \
            -> None:
        """Add validation result objects to a list of results.

        :param list classification_tokens: A list of Tokens
        :param list transcripts: A list of transcript strings
        :param Classification classification: A classification for a list of
            tokens
        :param list results: A list to store validation result objects
        :param list gene_tokens: List of GeneMatchTokens
        """
        valid_alleles = list()
        mane_transcripts_dict = dict()
        for s in classification_tokens:
            for t in transcripts:
                errors = list()

                if 'HGVS' in classification.matching_tokens:
                    hgvs_expr, is_ensembl_transcript = \
                        self.get_hgvs_expr(classification, t, s, True)
                    allele = self.get_allele_from_hgvs(hgvs_expr, errors)
                    t = hgvs_expr.split(':')[0]
                else:
                    hgvs_expr, is_ensembl_transcript = \
                        self.get_hgvs_expr(classification, t, s, False)
                    allele = self.get_allele_from_hgvs(hgvs_expr, errors)

                if allele:
                    mane_transcripts_dict[hgvs_expr] = {
                        'classification_token': s,
                        'transcript_token': t,
                        'is_ensembl_transcript': is_ensembl_transcript
                    }

                    ref_sequence = self.get_reference_sequence(t, s, errors)

                    if ref_sequence and s.deleted_sequence:
                        self.check_reference_sequence(
                            ref_sequence, s.deleted_sequence, errors
                        )

                self.add_validation_result(
                    allele, valid_alleles, results,
                    classification, s, t, gene_tokens, errors
                )

        # Now add Mane transcripts to results
        self.add_mane_transcript(classification, results, gene_tokens,
                                 mane_transcripts_dict)

    def get_gene_tokens(self, classification) -> List[GeneMatchToken]:
        """Return gene tokens for a classification.

        :param Classification classification: The classification for tokens
        :return: A list of Gene Match Tokens in the classification
        """
        return self.get_gene_symbol_tokens(classification)

    def variant_name(self):
        """Return the variant name."""
        return 'genomic deletion'

    def is_token_instance(self, t):
        """Check that token is Genomic Deletion."""
        return t.token_type == 'GenomicDeletion'

    def validates_classification_type(
            self,
            classification_type: ClassificationType) -> bool:
        """Return whether or not the classification type is
        Genomic DelIns.
        """
        return classification_type == ClassificationType.GENOMIC_DELETION

    def human_description(self, transcript,
                          token: GenomicDeletionToken) -> str:
        """Return a human description of the identified variant."""
        if token.start_pos_del is not None and token.end_pos_del is not None:
            position = f"{token.start_pos_del} to {token.end_pos_del}"
        else:
            position = token.start_pos_del

        descr = "A Genomic "
        if token.deleted_sequence:
            descr += f"{token.deleted_sequence} "
        descr += f"Deletion from {position} on transcript {transcript}"
        return descr
