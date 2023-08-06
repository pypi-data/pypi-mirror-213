#===============================================================================
# plot_bedtools.py
#===============================================================================

def generate_feature_data(bedtool, chromosomes=None):
    """Generate (as tuples) entries from a bedtool object containing
    methylation data

    Parameters
    ----------
    bedtool
        a BedTool object
    chromosomes
        iterable of chromosomes to include in results, or None to include
        all chromosomes

    Yield
    -----
    tuple
    """

    if chromosomes is not None:
        chromosomes = set(chromosomes)
    for i in bedtool:
        n_fields = len(i.fields)
        if n_fields == 17:
            chrom, _, _, _, _, _, _, _, _, coverage, meth, _, start, end, strand, gene, _ = i.fields
        elif n_fields == 15:
            chrom, _, _, meth, _, coverage, _, _, _, _, start, end, strand, gene, _ = i.fields
        else:
            raise RuntimeError('Invalid methylation BED file')
        if (chromosomes is None) or (chrom in chromosomes):
            yield chrom, int(start), int(end), gene, strand, 1, int(coverage), float(meth)


def generate_plotting_data(bedtools, groups, scale: float = 1,
                           shift: float = 0, smooth: bool = False):
    """Generate methylation data converted to plotting coordinates for gene
    or TE profile plots

    Parameters
    ----------
    bedtools
        iterable of bedtools containing methylation data
    groups
        iterable of group names for input datasets
    scale : float
        ratio of chromosome size to mean chromosome size
    shift : float
        x-axis shift of this chromosome, for plots showing multiple chromosomes
        consecutively
    smooth : bool
        if True, draw a smoother plot
    """

    for bt, g in zip(bedtools, groups):
        for i in bt:
            n_fields = len(i.fields)
            if n_fields == 17:
                _, _, pos, _, _, _, _, _, _, _, meth, _, start, end, strand, index, _, group = i.fields+[g]
            elif n_fields == 15:
                _, _, pos, meth, _, _, _, _, _, _, start, end, strand, index, _, group = i.fields+[g]
            else:
                raise RuntimeError('Invalid methylation BED file')
            yield (round((int(pos)-int(start) if strand == '+' else int(end)-int(pos))
         / (int(end)-int(start)), 2-smooth)*scale + shift, float(meth), group, index)
