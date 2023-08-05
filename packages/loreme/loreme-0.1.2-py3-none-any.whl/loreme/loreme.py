#===============================================================================
# loreme.py
#===============================================================================

"""Process PacBio or Nanopore methylation data"""




# Imports ======================================================================

import argparse
import os.path
import platform
from math import floor
from loreme.env import (PBCPG_DIR, PBCPG_MODEL, EXAMPLE_DATA_DIR, DORADO_DIR,
                       DORADO_MODEL_DIR)
from loreme.version import __version__
from loreme.download import download_pbcpg, download_example, download_dorado
from loreme.pbcpg import pbcpg_check_tags, pbcpg_align_bams, pbcpg_extract
from loreme.check_gpu_availability import check_gpu_availability
from loreme.dorado import fast5_to_pod5, dorado, dorado_align
from loreme.mean import calculate_mean, calculate_total_mean
from loreme.gene_body_methylation import gene_body_methylation
from loreme.promoter_methylation import promoter_methylation
from loreme.plot import plot, COLOR_PALETTE
from loreme.plot_genes import plot_genes
from loreme.plot_repeats import plot_repeats
from loreme.merge import merge_bedmethyl
from loreme.intersect import intersect_bedmethyl
from loreme.export_bedgraph import export_bedgraph




# Functions ====================================================================

def error_exit(msg):
    """Exit with an error

    Parameters
    ----------
    msg : str
        String describing the error
    """

    raise RuntimeError(msg)


def pbcpg_validate_args_pre_alignment(args):
    """Validate arguments before the alignment step

    Parameters
    ----------
    args
        argparse.Namespace containing the arguments
    """

    def check_required_file(file, label):
        if not os.path.isfile(file):
            error_exit(f"Can't find {label} file '{file}'")
    for bam in args.bam:
        check_required_file(bam, "input bam")
    check_required_file(args.fasta, "reference fasta")
    if not os.path.isfile(args.model):
        error_exit("{} is not a valid model file!".format(args.model))


def pbcpg_validate_args_post_alignment(args):
    """Validate arguments after the alignment step

    Parameters
    ----------
    args
        argparse.Namespace containing the arguments
    """

    def is_bam_index_found(bam_file):
        bam_index_extensions = (".bai", ".csi")
        for ext in bam_index_extensions:
            bam_index_file=bam_file+ext
            if os.path.isfile(bam_index_file):
                return True
        return False
    if not is_bam_index_found(args.bam):
        error_exit(f"Can't find index for bam file '{args.bam}'")


def _download_pbcpg(args):
    download_pbcpg(directory=args.directory)


def _download_example(args):
    download_example(directory=args.directory, n_samples=args.n_samples)


def _download_dorado(args):
    download_dorado(args.platform, directory=args.directory,
                    model_dir=args.model_dir)


def _pbcpg_check_tags(args):
    if pbcpg_check_tags(args.bam, n_reads=args.n_reads):
        print('MM/ML tags found')
    else:
        raise RuntimeError('MM/ML tags not found in BAM file')


def _pbcpg_align(args):
    pbcpg_align_bams(args.fasta, args.bam, args.aligned_bam,
        threads=max(1, args.threads-1),
        memory_mb=max(floor(args.memory/args.threads), 1))


def _pbcpg_extract(args):
    pbcpg_extract(args.bam, args.output_prefix, hap_tag=args.hap_tag,
                  min_coverage=args.min_coverage,min_mapq=args.min_mapq,
                  model=args.model, threads=args.threads)


def run_pbcpg(args):
    pbcpg_validate_args_pre_alignment(args)
    for bam in args.bam:
        if not pbcpg_check_tags(bam, n_reads=args.n_reads):
            raise RuntimeError('MM/ML tags not found in BAM file')
    aligned_bam = f'{args.output_prefix}.pbmm2.bam'
    pbcpg_align_bams(args.fasta, args.bam, aligned_bam,
        threads=max(1, args.threads-1),
        memory_mb = max(floor(args.memory/args.threads), 1))
    args.bam = aligned_bam
    pbcpg_validate_args_post_alignment(args)
    _pbcpg_extract(args)


def _fast5_to_pod5(args):
    fast5_to_pod5(*args.fast5, output_pod5=args.output, threads=args.threads)


def _dorado_check_gpu(args):
    if check_gpu_availability(args.devices, gpu_load=args.gpu_load,
                           gpu_mem=args.gpu_mem):
        print('GPU is available')


def _dorado_align(args):
    dorado_align(args.index, args.reads, args.output)


def run_dorado(args):
    check_gpu_availability([0])
    if args.convert:
        pod5_dir = f'{args.output[:-4]}_pod5'
        pod5_base = f'{os.path.basename(args.output)[:-4]}.pod5'
        os.mkdir(pod5_dir)
        fast5_to_pod5(*args.reads,
                      output_pod5=os.path.join(pod5_dir, pod5_base),
                      threads=args.threads)
        dorado(pod5_dir, args.output, speed=args.speed, accuracy=args.accuracy)
    elif len(args.reads) == 1 and os.path.isdir(args.reads[0]):
        dorado(args.reads[0], args.output, speed=args.speed,
               accuracy=args.accuracy)
    else:
        raise RuntimeError('For running without --convert, supply only one input FAST5 or POD5 directory')



def _calculate_mean(args):
    if args.total:
        calculate_total_mean(args.bedmethyl, plot=args.plot,
                             groups=args.groups, title=args.title,
                             legend_title=args.legend_title, width=args.width,
                             color_palette=args.color_palette)
    else:
        calculate_mean(args.bedmethyl, plot=args.plot,
                       chromosomes=args.chromosomes, groups=args.groups,
                       title=args.title, legend_title=args.legend_title,
                       width=args.width, color_palette=args.color_palette)


def _promoter_methylation(args):
    promoter_methylation(args.features, args.bedmethyl,
        upstream_flank=args.upstream_flank,
        downstream_flank=args.downstream_flank, chromosomes=args.chromosomes,
        cytosines=args.cytosines, coverage=args.coverage,
        min_coverage=args.min_coverage, bins=args.bins, levels=args.levels,
        hist=args.hist, hist_log=args.hist_log, palette=args.palette)


def _gene_body_methylation(args):
    gene_body_methylation(args.features, args.bedmethyl,
        upstream_flank=args.upstream_flank,
        downstream_flank=args.downstream_flank, chromosomes=args.chromosomes,
        cytosines=args.cytosines, coverage=args.coverage,
        min_coverage=args.min_coverage, bins=args.bins, levels=args.levels,
        hist=args.hist, hist_log=args.hist_log, palette=args.palette)

def _plot(args):
    plot(args.bedmethyl, args.output, reference=args.reference,
         chromosomes=args.chromosomes, groups=args.groups, title=args.title,
         legend=args.legend, legend_title=args.legend_title,
         bin_size=args.bin_size, width=args.width,
         color_palette=args.color_palette, alpha=args.alpha,
         x_label=args.x_label)


def _plot_genes(args):
    plot_genes(args.features, args.bedmethyl, args.output, groups=args.groups,
               flank=args.flank, smooth=args.smooth, title=args.title,
               confidence_interval=args.confidence_interval,
               gene_bins=args.gene_bins, gene_levels=args.gene_levels,
               legend=args.legend, legend_title=args.legend_title,
               palette=args.palette, width=args.width, alpha=args.alpha)


def _plot_repeats(args):
    plot_repeats(args.features, args.bedmethyl, args.output, type=args.type,
                 groups=args.groups, flank=args.flank, smooth=args.smooth,
                 title=args.title, confidence_interval=args.confidence_interval,
                 legend=args.legend, legend_title=args.legend_title,
                 palette=args.palette, width=args.width, alpha=args.alpha)

def _merge(args):
    merge_bedmethyl(args.bedmethyl, chromosomes=args.chromosomes)


def _intersect(args):
    intersect_bedmethyl(args.bedmethyl, chromosomes=args.chromosomes)


def _export_bedgraph(args):
    export_bedgraph(args.bedmethyl, chromosomes=args.chromosomes,
                    coverage=args.coverage)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""Analysis of DNA methylation signals from `Pacific Biosciences <https://www.pacb.com/technology/hifi-sequencing/>`_
or `Oxford Nanopore <https://nanoporetech.com/applications/dna-nanopore-sequencing>`_
long read sequencing data.""")
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
    subparsers = parser.add_subparsers()

    parser_download_pbcpg = subparsers.add_parser('download-pbcpg',
                                                  help='download pb-CpG-tools')
    parser_download_pbcpg.set_defaults(func=_download_pbcpg)
    parser_download_pbcpg.add_argument(
        '-d', '--directory', metavar='<directory/>', default=PBCPG_DIR,
        help=f'destination directory for pb-CpG-tools (default: {PBCPG_DIR})')

    parser_download_dorado = subparsers.add_parser('download-dorado',
                                                  help='download dorado')
    parser_download_dorado.set_defaults(func=_download_dorado)
    parser_download_dorado.add_argument(
        'platform', choices=('linux-x64', 'linux-arm64', 'osx-arm64', 'win64'),
        help=f'Select your platform. If you\'re unsure, the following information about your system and machine may help you choose. system: {platform.system()}, machine: {platform.machine()}')
    parser_download_dorado.add_argument(
        '-d', '--directory', metavar='<directory/>', default=DORADO_DIR,
        help=f'destination directory for dorado (default: {DORADO_DIR})')
    parser_download_dorado.add_argument(
        '-m', '--model-dir', metavar='<directory/>', default=DORADO_MODEL_DIR,
        help=f'destination directory for dorado models (default: {DORADO_MODEL_DIR})')

    parser_download_example = subparsers.add_parser('download-example',
        help='download an example dataset for pbcpg')
    parser_download_example.set_defaults(func=_download_example)
    parser_download_example.add_argument( '-d', '--directory', metavar='<directory/>',
        default=EXAMPLE_DATA_DIR, help='destination directory for example data')
    parser_download_example.add_argument('-n', '--n-samples', metavar='<int>',
        type=int, default=1, help='number of samples to download, max 4 (default: 1)')

    parser_pbcpg = subparsers.add_parser('pbcpg', help='run full pbcpg pipeline')
    parser_pbcpg.set_defaults(func=run_pbcpg)
    io_args = parser_pbcpg.add_argument_group('io args')
    io_args.add_argument("bam", metavar="<unaligned.bam>", nargs='+',
                        help="Unaligned BAM file.")
    io_args.add_argument("fasta", metavar="<ref.fasta>",
                        help="The reference fasta file.")
    io_args.add_argument("output_prefix", metavar="<prefix>",
                        help="Label for output files, which results in [prefix].bam/bed/bw.")
    score_args = parser_pbcpg.add_argument_group('score args')
    score_args.add_argument("--model", metavar="</path/to/model.tflite>",
                        default=PBCPG_MODEL,
                        help=f"Full path to the directory containing the model to load. (default: {PBCPG_MODEL})")
    score_args.add_argument("-m", "--modsites", choices=["denovo", "reference"],
                        default="denovo",
                        help="Only output CG sites with a modification probability > 0 "
                             "(denovo), or output all CG sites based on the "
                             "supplied reference fasta (reference). (default: %(default)s)")
    score_args.add_argument("-c", "--min_coverage", metavar="<int>", default=4,
                        type=int,
                        help="Minimum coverage required for filtered outputs. (default: %(default)d)")
    score_args.add_argument("-q", "--min-mapq", metavar="<int>", default=0,
                        type=int,
                        help="Ignore alignments with MAPQ < N. (default: %(default)d)")
    score_args.add_argument("-a", "--hap-tag", metavar="<TAG>", default="HP",
                        help="The SAM tag containing haplotype information. (default: %(default)s)")
    score_args.add_argument("-s", "--chunksize", metavar="<int>", default=500_000,
                        type=int,
                        help="Break reference regions into chunks "
                             "of this size for parallel processing. (default: %(default)d)")
    score_args.add_argument('-n', '--n-reads', metavar="<int>",
                        type=int, default=1000,
                        help="Number of reads for MM/ML tag check. (default: %(default)d)")
    resource_args = parser_pbcpg.add_argument_group('resource args')
    resource_args.add_argument("-t", "--threads", metavar="<int>", default=1,
                        type=int,
                        help="Number of threads for parallel processing. (default: %(default)d)")
    resource_args.add_argument("--memory", metavar="<int>", default=4_000,
                        type=int,
                        help="Memory for read alignment and sorting in megabytes. (default: %(default)d)")
    
    parser_pbcpg_check = subparsers.add_parser('pbcpg-check', help='check BAM for MM/ML tags')
    parser_pbcpg_check.set_defaults(func=_pbcpg_check_tags)
    parser_pbcpg_check.add_argument("bam", metavar="<reads.bam>",
        help="BAM file to check.")
    parser_pbcpg_check.add_argument('-n', '--n-reads', metavar="<int>",
        type=int, default=1000, help="Number of reads to check (default: %(default)d].")

    parser_pbcpg_align = subparsers.add_parser('pbcpg-align', help='align BAM to reference')
    parser_pbcpg_align.set_defaults(func=_pbcpg_align)
    io_args = parser_pbcpg_align.add_argument_group('io args')
    io_args.add_argument("bam", metavar="<unaligned.bam>", nargs='+',
        help="Unaligned BAM file to read.")
    io_args.add_argument("fasta", metavar="<ref.fasta>",
        help="The reference fasta file.")
    io_args.add_argument("aligned_bam", metavar="<aligned.bam>",
        help="Aligned bam file to write.")
    resource_args = parser_pbcpg_align.add_argument_group('resource args')
    resource_args.add_argument("-t", "--threads", metavar="<int>", type=int,
        default=1,
        help="Number of threads for parallel processing. (default: %(default)d)")
    resource_args.add_argument("--memory", metavar="<int>", type=int,
        default=4_000,
        help="Memory for read alignment and sorting in megabytes. (default: %(default)d)")

    parser_pbcpg_extract = subparsers.add_parser('pbcpg-extract', help='extract methylation calls from aligned PB reads')
    parser_pbcpg_extract.set_defaults(func=pbcpg_extract)
    io_args = parser_pbcpg_extract.add_argument_group('io args')
    io_args.add_argument("bam", metavar="<aligned.bam>",
                        help="Aligned BAM file.")
    io_args.add_argument("fasta", metavar="<ref.fasta>",
                        help="The reference fasta file.")
    io_args.add_argument("output_prefix", metavar="<prefix>",
                        help="prefix for output files, which results in [prefix].bam/bed/bw.")
    score_args = parser_pbcpg_extract.add_argument_group('score args')
    score_args.add_argument("--model", metavar="</path/to/model.tflite>",
                        default=PBCPG_MODEL,
                        help=f"Full path to the model (*.tflite files) to load. (default: {PBCPG_MODEL})")
    score_args.add_argument("--modsites", choices=["denovo", "reference"],
                        default="denovo",
                        help="Only output CG sites with a modification probability > 0 "
                             "(denovo), or output all CG sites based on the "
                             "supplied reference fasta (reference). (default: %(default)s)")
    score_args.add_argument("-c", "--min_coverage", metavar="<int>", default=4,
                        type=int,
                        help="Minimum coverage required for filtered outputs. (default: %(default)d)")
    score_args.add_argument("-q", "--min_mapq", metavar="<int>", default=0,
                        type=int,
                        help="Ignore alignments with MAPQ < N. (default: %(default)d)")
    score_args.add_argument("-a", "--hap_tag", metavar="<TAG>", default="HP",
                        help="The SAM tag containing haplotype information. (default: %(default)s)")
    score_args.add_argument("-s", "--chunksize", metavar="<int>", default=500_000,
                        type=int,
                        help="Break reference regions into chunks "
                             "of this size for parallel processing. (default: %(default)d)")
    resource_args = parser_pbcpg_extract.add_argument_group('resource args')
    resource_args.add_argument("-t", "--threads", metavar="<int>", default=1,
                        type=int,
                        help="Number of threads for parallel processing. (default: %(default)d)")
    
    parser_dorado = subparsers.add_parser('dorado',
        help='run full dorado pipeline')
    parser_dorado.set_defaults(func=run_dorado)
    parser_dorado.add_argument('reads', metavar='<reads>', nargs='+',
                               help='input FAST5 files, or single directory containing FAST5 or POD5 files')
    parser_dorado.add_argument('output', metavar='<output.sam>',
                               help='path to output SAM file')
    parser_dorado.add_argument('--convert', action='store_true',
                               help='convert FAST5 to POD5 before basecalling')
    parser_dorado.add_argument('--speed', type=int, choices=(260, 400),
                               default=400, help='pore speed (default: 400)')
    parser_dorado.add_argument('--accuracy', choices=('fast', 'hac', 'sup'),
                               default='fast', help='model accuracy (default: fast)')
    # parser_dorado.add_argument('--frequency', choices=('4kHz', '5kHz'),
    #                            default='4kHz', help='(default: 4kHz)')
    # parser_dorado.add_argument('--modified-bases',
    #                            choices=('5mCG_5hmCG', '5mC', '6mA'),
    #                            default='5mCG_5hmCG',
    #                            help='Modified base model (default: 5mCG_5hmCG)')
    # parser_dorado.add_argument('--reference', metavar='<index>',
    #                            help='map to a reference index (fastq/fasta/mmi)')
    parser_dorado.add_argument("-t", "--threads", metavar="<int>",
        type=int, default=1,
        help="Number of cpu threads. (default: %(default)d)")
    
    parser_dorado_check = subparsers.add_parser('dorado-check',
        help='check GPU availability')
    parser_dorado_check.set_defaults(func=_dorado_check_gpu)
    parser_dorado_check.add_argument('--devices', metavar='<int>', type=int,
                                      nargs='+', default=[0],
                                      help='GPUs to check')
    parser_dorado_check.add_argument('--gpu-load', metavar='<float>', type=float,
                                     default=0.9,
                                     help='required available GPU load')
    parser_dorado_check.add_argument('--gpu-mem', metavar='<float>', type=float,
                                     default=0.9,
                                     help='required available GPU memory')

    parser_dorado_convert = subparsers.add_parser('dorado-convert',
        help='convert FAST5 to POD5')
    parser_dorado_convert.set_defaults(func=_fast5_to_pod5)
    parser_dorado_convert.add_argument('fast5', metavar='<reads[.fast5]>', nargs='+',
                               help='input FAST5 files, or direcories containing FAST5')
    parser_dorado_convert.add_argument('output', metavar='<output.pod5>',
                               help='path to output POD5 file')
    parser_dorado_convert.add_argument("-t", "--threads", metavar="<int>",
        type=int, default=1, help="Number of threads. (default: %(default)d)")

    parser_dorado_align = subparsers.add_parser('dorado-align',
        help='align dorado basecalls')
    parser_dorado_align.set_defaults(func=_dorado_align)
    parser_dorado_align.add_argument('index', metavar='<index>',
                                     help='reference index for alignment')
    parser_dorado_align.add_argument('reads', metavar='<reads>',
                                     help='reads for alignment')
    parser_dorado_align.add_argument('output', metavar='<output.bam>',
                                     help='path to output BAM file')

    parser_mean = subparsers.add_parser('mean',
        help='calculate average methylation across chromosomes or in total')
    parser_mean.set_defaults(func=_calculate_mean)
    parser_mean.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_mean.add_argument('--plot', metavar='<output.{pdf,png,svg}>',
        help='path to output plot')
    domain_group = parser_mean.add_mutually_exclusive_group()
    domain_group.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to include')
    domain_group.add_argument('--total', action='store_true',
        help='calculate total genomic mean')
    parser_mean.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files [0)')
    parser_mean.add_argument('--title', metavar='<"Plot title">',
        default='Methylation', help='set the title for the plot')
    parser_mean.add_argument('--legend-title', metavar='<Title>',
        default='Group', help='title of legend')
    parser_mean.add_argument('--width', metavar='<float>', type=float,
        default=8, help='set width of figure in inches')
    parser_mean.add_argument('--color-palette', metavar='<#color>', nargs='+',
        default=COLOR_PALETTE, help='color palette to use')

    parser_promoter = subparsers.add_parser('promoter',
        help='quantify promoter methylation')
    parser_promoter.set_defaults(func=_promoter_methylation)
    parser_promoter.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_promoter.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        help='bedMethyl file containing methylation data')
    parser_promoter.add_argument('--upstream-flank', metavar='<int>', type=int,
        default=2000, help='length of upstream flank in bp (default: 2000)')
    parser_promoter.add_argument('--downstream-flank', metavar='<int>',
        type=int, default=0, help='length of upstream flank in bp (default: 0)')
    parser_promoter.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to include')
    parser_promoter.add_argument('--cytosines', action='store_true',
        help='output a column with number of cytosines in each promoter')
    parser_promoter.add_argument('--coverage', action='store_true',
        help='output a column of coverage for each promoter')
    parser_promoter.add_argument('--min-coverage', metavar='<int>',
        type=int, default=1, help='minimum coverage to include promoter [1)')
    parser_promoter.add_argument('--bins', action='store_true',
        help='output a column binning promoters by discrete methylation level')
    parser_promoter.add_argument('--levels', metavar='<Level>',
        nargs='+', default=['Min', 'Low', 'Mid', 'High', 'Max'],
        help='discrete methylation levels')
    parser_promoter.add_argument('--hist', metavar='<file.{pdf,png,svg}>',
        help='generate histogram of methylation levels')
    parser_promoter.add_argument('--hist-log', action='store_true',
        help='use a log scale for  histogram')
    parser_promoter.add_argument('--palette', metavar='<palette>',
        default='mako_r', help='name of seaborn color palette (default: mako_r)')

    parser_gene_body = subparsers.add_parser('gene-body',
        help='quantify gene body methylation')
    parser_gene_body.set_defaults(func=_gene_body_methylation)
    parser_gene_body.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_gene_body.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        help='bedMethyl file containing methylation data')
    parser_gene_body.add_argument('--upstream-flank', metavar='<int>', type=int,
        default=0, help='length of upstream flank in bp (default: 0)')
    parser_gene_body.add_argument('--downstream-flank', metavar='<int>',
        type=int, default=0, help='length of upstream flank in bp (default: 0)')
    parser_gene_body.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to include')
    parser_gene_body.add_argument('--cytosines', action='store_true',
        help='output a column with number of cytosines in each gene')
    parser_gene_body.add_argument('--coverage', action='store_true',
        help='output a column of coverage for each gene')
    parser_gene_body.add_argument('--min-coverage', metavar='<int>',
        type=int, default=1, help='minimum coverage to include gene (default: 1)')
    parser_gene_body.add_argument('--bins', action='store_true',
        help='output  a column binning genes by discrete methylation level')
    parser_gene_body.add_argument('--levels', metavar='<Level>',
        nargs='+', default=['Min', 'Low', 'Mid', 'High', 'Max'],
        help='discrete methylation levels')
    parser_gene_body.add_argument('--hist', metavar='<file.{pdf,png,svg}>',
        help='generate histogram of methylation levels')
    parser_gene_body.add_argument('--hist-log', action='store_true',
        help='use a log scale for  histogram')
    parser_gene_body.add_argument('--palette', metavar='<palette>',
        default='mako_r', help='name of seaborn color palette (default: mako_r)')
    
    parser_plot = subparsers.add_parser('plot',
        help='plot methylation across chromosomes')
    parser_plot.set_defaults(func=_plot)
    parser_plot.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_plot.add_argument('output', metavar='<output.{pdf,png,svg}>',
        help='path to output file')
    parser_plot.add_argument('--reference', metavar='<reference.fa>',
        help='reference genome')
    parser_plot.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to plot')
    parser_plot.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files (default: 0)')
    parser_plot.add_argument('--title', metavar='<"Plot title">',
        default='Methylation', help='set the title for the plot')
    parser_plot.add_argument('--x-label', metavar='<"Label">',
        default='Chromosome', help='set x-axis label for the plot (default: Chromosome)')
    parser_plot.add_argument('--legend', action='store_true',
        help='include a legend with the plot')
    parser_plot.add_argument('--legend-title', metavar='<"Title">',
        default='Group', help='title of legend')
    parser_plot.add_argument('--bin-size', metavar='<int>', type=int, default=0,
        choices=(-2,-1,0,1,2),
        help=('Set bin size. The input <int> is converted to the bin size by '
              'the formula: 10^(<int>+6) bp. The default value is 0, i.e. '
              '1-megabase bins. (default: 0)'))
    parser_plot.add_argument('--width', metavar='<float>', type=float,
        default=8.0, help='set width of figure in inches (default: 8.0)')
    parser_plot.add_argument('--color-palette', metavar='<#color>', nargs='+',
        default=COLOR_PALETTE, help='color palette to use')
    parser_plot.add_argument('--alpha', metavar='<float>', type=float,
        default=0.5, help='transparency value for lines (default: 0.5)')
    
    parser_plot_genes = subparsers.add_parser('plot-genes',
        help='plot methylation profiles over genomic features')
    parser_plot_genes.set_defaults(func=_plot_genes)
    parser_plot_genes.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_plot_genes.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_plot_genes.add_argument('output', metavar='<output.{pdf,png,svg}>',
        help='path to output file')
    parser_plot_genes.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files [0)')
    parser_plot_genes.add_argument('--flank', metavar='<int>', type=int,
        default=2000, help='size of flanking regions in bp [1000)')
    parser_plot_genes.add_argument('--smooth', action='store_true',
        help='draw a smoother plot')
    parser_plot_genes.add_argument('--confidence-interval', metavar='<int>',
        type=int, help='draw a confidence interval')
    parser_plot_genes.add_argument('--title', metavar='<"Plot title">',
        default='Methylation',
        help='set the title for the plot')
    parser_plot_genes.add_argument('--gene-bins', metavar='<gene_bins.json>',
        help='gene bins')
    parser_plot_genes.add_argument('--gene-levels', metavar='<Level>',
        nargs='+', default=['Min', 'Low', 'Mid', 'High', 'Max'],
        help='gene expression levels')
    parser_plot_genes.add_argument('--legend', action='store_true',
        help='include a legend with the plot')
    parser_plot_genes.add_argument('--legend-title', metavar='<Title>',
        default='Group', help='title of legend')
    parser_plot_genes.add_argument('--width', metavar='<float>', type=float,
        default=4.0, help='set width of figure in inches (default: 4.0)')
    parser_plot_genes.add_argument('--palette', metavar='<palette>',
        default='deep', help='name of seaborn color palette (default: deep)')
    parser_plot_genes.add_argument('--alpha', metavar='<float>', type=float,
        default=1.0, help='transparency value for lines (default: 1.0)')
    
    parser_plot_repeats = subparsers.add_parser('plot-repeats',
        help='plot methylation profiles over genomic features')
    parser_plot_repeats.set_defaults(func=_plot_repeats)
    parser_plot_repeats.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_plot_repeats.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_plot_repeats.add_argument('output', metavar='<output.{pdf,png,svg}>',
        help='path to output file')
    parser_plot_repeats.add_argument('--type', metavar='<"feature_type">',
        help='generate plot for a specific type of repeat')
    parser_plot_repeats.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files (default: 0)')
    parser_plot_repeats.add_argument('--flank', metavar='<int>', type=int,
        default=500, help='size of flanking regions in bp (default: 500)')
    parser_plot_repeats.add_argument('--smooth', action='store_true',
        help='draw a smoother plot')
    parser_plot_repeats.add_argument('--confidence-interval', metavar='<int>',
        type=int, help='draw a confidence interval')
    parser_plot_repeats.add_argument('--title', metavar='<"Plot title">',
        default='Methylation',
        help='set the title for the plot')
    parser_plot_repeats.add_argument('--legend', action='store_true',
        help='include a legend with the plot')
    parser_plot_repeats.add_argument('--legend-title', metavar='<Title>',
        default='Group', help='title of legend (default: Group)')
    parser_plot_repeats.add_argument('--width', metavar='<float>', type=float,
        default=4.0, help='set width of figure in inches (default: 4.0)')
    parser_plot_repeats.add_argument('--palette', metavar='<palette>',
        default='deep', help='name of seaborn color palette (default: deep)')
    parser_plot_repeats.add_argument('--alpha', metavar='<float>', type=float,
        default=1, help='transparency value for lines (default: 1.0)')
    
    parser_intersect = subparsers.add_parser('intersect',
        help='intersect two or more bedmethyl files')
    parser_intersect.set_defaults(func=_intersect)
    parser_intersect.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_intersect.add_argument('output_prefix', metavar='<output-prefix>',
        help='prefix for output files')
    parser_intersect.add_argument('--chromosomes', metavar='<X>',
        nargs='+', help='chromosomes to include')

    return parser.parse_args()


def main():
    args = parse_arguments()
    args.func(args)
