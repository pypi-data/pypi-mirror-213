# LoReMe pipeline

TODO: make a 'loreme clean' subcommand to remove downloads before uninstalling

LoReMe (Long Read Methylaton) is a Python package facilitating analysis of
DNA methylation signals from [Pacific Biosciences](https://www.pacb.com/technology/hifi-sequencing/)
or [Oxford Nanopore](https://nanoporetech.com/applications/dna-nanopore-sequencing)
long read sequencing data.

It consists of an API and CLI for three distinct applications:

1. Pacific Biosciences data processing. PB reads in SAM/BAM format are aligned
to a reference genome with the special-purpose aligner [pbmm2](https://github.com/PacificBiosciences/pbmm2>),
a modified version of [minimap2](https://lh3.github.io/minimap2/).
Methylation calls are then extracted from the aligned reads by [pb-CpG-tools](https://github.com/PacificBiosciences/pb-CpG-tools).

2. Oxford nanopore basecalling. ONT reads are optionally converted from FAST5
to [POD5](https://github.com/nanoporetech/pod5-file-format) format, then
basecalled and aligned to a reference with [dorado](https://github.com/nanoporetech/dorado>).
(dorado alignment also uses minimap2 under the hood).

3. Postprocessing and QC of methylation calls. Several functions are available
to generate diagnostic statistics and plots.

See also the [full documentation](https://salk-tm.gitlab.io/loreme/index.html).

Other tools of interest: [methylartist](https://github.com/adamewing/methylartist) and [modbamtools](https://github.com/rrazaghi/modbamtools)  ([modbamtools docs](https://rrazaghi.github.io/modbamtools/)), [methplotlib](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7214038/)

## Installation

### Conda

The recommended way to install `loreme` is with a dedicated `conda` environment:

First create an environment including all dependencies:
```
conda create -n loreme -c conda-forge -c bioconda pbmm2 urllib3 \
  pybedtools gff2bed seaborn pyfaidx psutil gputil tabulate \
  cython h5py iso8601 more-itertools polars tqdm
conda activate loreme
```

Then install with `pip`:
```
pip install loreme
```

Alternatively, install from the git repo:
```
git clone https://gitlab.com/salk-tm/loreme.git
cd loreme
pip install .
```

You may also wish to install `nvtop` to monitor GPU usage:
```
conda install -c conda-forge nvtop
```

### Check installation

Check that the correct version was installed with `loreme --version`
