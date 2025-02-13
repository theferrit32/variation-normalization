"""A module for testing Silent Mutation tokenization."""
import unittest

from variation.tokenizers import SilentMutation
from .tokenizer_base import TokenizerBase


class TestSilentMutationTokenizer(TokenizerBase, unittest.TestCase):
    """A class for testing Silent Mutation Tokenization."""

    def tokenizer_instance(self):
        """Return Silent Mutation instance."""
        return SilentMutation()

    def token_type(self):
        """Return Silent Mutation token type."""
        return "SilentMutation"

    def fixture_name(self):
        """Return the fixture name for Silent Mutation."""
        return "silent_mutation"
