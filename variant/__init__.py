"""The Variant Normalization package."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEQREPO_DATA_PATH = f"{PROJECT_ROOT}/variant/data/seqrepo/latest"
TRANSCRIPT_MAPPINGS_PATH = f"{PROJECT_ROOT}/variant/data/transcript_mapping.tsv"  # noqa: E501
AMINO_ACID_PATH = f"{PROJECT_ROOT}/variant/data/amino_acids.csv"
GENE_SYMBOL_PATH = f"{PROJECT_ROOT}/variant/data/gene_symbols.txt"