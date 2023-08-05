#===============================================================================
# parse_gff.py
#===============================================================================

def generate_flank(genes_df, side: str = 'up', flank: int = 1000):
    """Generate coordinates of upstream or downstream flanks for input features

    Parameters
    ----------
    genes_df
        data frame containing gene coordinates
    side : str
        "up" for upstream flank, "down" for downstream flank
    flank : int
        size of flank in bp

    Yields
    ------
    tuple
        coordinates, strand, and gene ID corresponding to the flank
    """

    if side == 'up':
        for index, row in genes_df.iterrows():
            if row['strand'] == '+':
                yield row['seqid'], int(row['start'] - flank), row['start'], '+', index
            elif row['strand'] == '-':
                yield row['seqid'], row['end'], int(row['end'] + flank), '-', index
    elif side == 'down':
        for index, row in genes_df.iterrows():
            if row['strand'] == '+':
                yield row['seqid'], row['end'], int(row['end'] + flank), '+', index
            elif row['strand'] == '-':
                yield row['seqid'], int(row['start'] - flank), row['start'], '-', index


def generate_feature_body(features_df, upstream_flank: int = 0, downstream_flank: int = 0):
    """Generate coordinates for bodies of input features

    Parameters
    ----------
    features_df
        data frame containing gene coordinates
    upstream_flank : int
        size of upstream region to include in body, in bp
    downstream_flank : int
        size of downstream region to include in body, in bp

    Yields
    ------
    tuple
        coordinates, strand, and feature ID corresponding to the feature body
    """

    for index, row in features_df.iterrows():
        if row['strand'] == '+':
            yield row['seqid'], int(row['start'] - upstream_flank) , int(row['end'] + downstream_flank), row['strand'], index
        if row['strand'] == '-':
            yield row['seqid'], int(row['start'] - downstream_flank) , int(row['end'] + upstream_flank), row['strand'], index


def generate_promoter(genes_df, upstream_flank: int = 2000, downstream_flank: int = 0):
    """Generate coordinates for promoters of input genes

    Parameters
    ----------
    genes_df
        data frame containing gene coordinates
    upstream_flank : int
        size of upstream region to include in promoter, in bp
    downstream_flank : int
        size of downstream region to include in promoter, in bp

    Yields
    ------
    tuple
        coordinates, strand, and feature ID corresponding to the promoter
    """

    for index, row in genes_df.iterrows():
        if row['strand'] == '+':
            yield row['seqid'], int(row['start'] - upstream_flank), int(row['start'] + downstream_flank), '+', index
        elif row['strand'] == '-':
            yield row['seqid'], int(row['end'] - downstream_flank), int(row['end'] + upstream_flank), '-', index
