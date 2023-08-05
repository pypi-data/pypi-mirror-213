#===============================================================================
# gene_body_methylation.py
#===============================================================================

"""Quantify gene body methylation"""

# Imports ======================================================================

from pybedtools import BedTool
import pandas as pd
import gff2bed

from loreme.parse_gff import generate_feature_body
from loreme.plot_bedtools import generate_feature_data
from loreme.methylation_hist import methylation_hist




# Functions ====================================================================

def gene_body_methylation(features, bedmethyl, upstream_flank: int = 0,
                         downstream_flank: int = 0, chromosomes=None,
                         cytosines: bool = False, coverage: bool = False,
                         min_coverage: bool = 1, bins: bool = False, hist=None,
                         levels=['Min', 'Low', 'Mid', 'High', 'Max'],
                         palette: str = 'mako_r', hist_log=False):
    """Quantify methylation in gene bodies

    Parameters
    ----------
    features
        path to GFF3 file containing gene coordinates
    bedmethyl
        path to bedmethyl formatted file containing methylation results
    upstream_flank : int
        size of upstream flank to include in gene body, in bp [0]
    downstream_flank : int
        size of downstream flank to include in gene body, in bp [0]
    chromosomes
        iterable of chromosomes to include, or None to include all chromosomes
    coverage : bool
        if True, include a coverage column in the results
    min_coverage : int
        minimum coverage for a gene to be included
    bins : bool
        if True, add an extra column binning genes by methylation level [False]
    hist
        if given, write a histogram of gene bin methylation levels
    hist_log
        if true, use a log scale for the histogram
    levels
        iterable of labels for binning by methylation level
    palette : str
        color palette for histogram
    """

    genes = pd.DataFrame((f for f in gff2bed.parse(features) if f[1] > upstream_flank),
        columns=('seqid', 'start', 'end', 'strand', 'attributes'))
    genes.index = (attr['ID'] for attr in genes['attributes'])
    gene_body = BedTool(tuple(generate_feature_body(genes,
        upstream_flank=upstream_flank, downstream_flank=downstream_flank)))
    methyl = BedTool(bedmethyl)
    methyl_gene_body = methyl.intersect(gene_body, wo=True)
    df = pd.DataFrame(
        generate_feature_data(methyl_gene_body, chromosomes=chromosomes),
        columns=('chrom', 'start', 'end', 'gene', 'strand', 'cytosines', 'coverage', 'methyl_sum')
    ).groupby(by=['chrom', 'start', 'end', 'gene', 'strand'], as_index=False).sum().sort_values(by=['chrom', 'start'])
    df.index = df['gene']
    df['Methylation level (%)'] = df['methyl_sum'] / df['cytosines']
    df['Discrete level'] = pd.qcut(df['Methylation level (%)'].rank(method='first'), q=len(levels), labels=levels)
    if hist:
        methylation_hist(df, hist, palette=palette, log_scale=hist_log)
    for _, (chrom, start, end, gene, strand, cyt, cov, methyl, level) in df.iloc[:,[0,1,2,3,4,5,6,8,9]].iterrows():
        row = (chrom, start, end, gene, f'{methyl:.2f}', strand) + cytosines*(cyt,) + coverage*(cov,) + bins*(level,)
        if cov >= min_coverage:
            print(*row, sep='\t')
