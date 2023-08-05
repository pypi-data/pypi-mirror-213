#===============================================================================
# methylation_hist.py
#===============================================================================

import seaborn as sns

def methylation_hist(df, output_file, palette='mako_r', log_scale=False):
    """Draw a histogram of methylation levels

    Parameters
    ----------
    df
        input data frame of methylation levels
    output_file
        path to output file
    palette
        color palette for discrete methylation levels
    xlog : bool
        if True, draw a log scale on the x-axis
    """

    ax = sns.histplot(data=df, x='Methylation level (%)',
                    hue='Discrete level', fill=True, palette=palette,
                    element='step', multiple='stack', log_scale=log_scale)
    fig = ax.get_figure()
    fig.set_figwidth(7)
    fig.set_figheight(3)
    fig.tight_layout()
    fig.savefig(output_file)
    fig.clf()
