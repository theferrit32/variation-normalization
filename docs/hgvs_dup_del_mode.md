# HGVS Dup Del Mode

This mode helps us interpret deletions and duplications that are represented as HGVS expressions.

## Default Characteristics

- If endpoints are ambiguous: cnv (copies attribute) 
    - handling X chromosome 
        - base 1-2 
            - Duplication: Definite Range =  2, 3 
            - Deletion: Definite Range =  0, 1 
    - handling Y chromosome 
        - base of 1  
            - Duplication: Number = 2 
            - Deletion: Number = 0 
    - handling 1 – 22 chromosome 
        - base of 2 
             - Duplication: Number = 3 
             - Deletion: Number = 1 
- elif len del or dup > 100bp: (use outermost coordinates) 
    - repeated_seq_expr with a derived_seq_expr subject (Allele) 
- else: 
    - literal_seq_expr (normalized LiteralSequenceExpression Allele) 

# Notes

- Ambiguous ranges are of the form:
    - `(#_#)_(#_#)`
    - `(?_#)_(#_?)`
    - `(?_#)_#`
    - `#_(#_?)`
- We do not normalize any ambiguous ranges
- We do not change the molecular context for ambiguous ranges.