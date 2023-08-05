"""LoReMe (Long Read Methylaton) is a Python package facilitating analysis of
DNA methylation signals from `Pacific Biosciences <https://www.pacb.com/technology/hifi-sequencing/>`_
or `Oxford Nanopore <https://nanoporetech.com/applications/dna-nanopore-sequencing>`_
long read sequencing data.

It consists of an API and CLI for three distinct applications:

1. Pacific Biosciences data processing. PB reads in SAM/BAM format are aligned
to a reference genome with the special-purpose aligner `pbmm2 <https://github.com/PacificBiosciences/pbmm2>`_ ,
a modified version of `minimap2 <https://lh3.github.io/minimap2/>`_ .
Methylation calls are then extracted from the aligned reads by `pb-CpG-tools <https://github.com/PacificBiosciences/pb-CpG-tools>`_ .

2. Oxford nanopore basecalling. ONT reads are optionally converted from FAST5
to `POD5 <https://github.com/nanoporetech/pod5-file-format>`_ format, then
basecalled and aligned to a reference with `dorado <https://github.com/nanoporetech/dorado>`_ .
(dorado alignment also uses minimap2 under the hood).

3. Postprocessing and QC of methylation calls. Several functions are available
to generate diagnostic statistics and plots.
"""

from loreme.version import __version__
from loreme.env import PBCPG_MODEL
from loreme.download import download_pbcpg, download_dorado
from loreme.pbcpg import pbcpg_check_tags, pbcpg_align_bam, pbcpg_align_bams, pbcpg_extract
from loreme.check_gpu_availability import check_gpu_availability
from loreme.dorado import dorado
