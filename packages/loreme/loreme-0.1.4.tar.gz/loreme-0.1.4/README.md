# LoReMe pipeline

LoReMe (Long Read Methylaton) is a Python package facilitating analysis of
DNA methylation signals from [Pacific Biosciences](https://www.pacb.com/technology/hifi-sequencing/)
or [Oxford Nanopore](https://nanoporetech.com/applications/dna-nanopore-sequencing)
long read sequencing data.

It consists of an API and CLI for three distinct applications:

1. Pacific Biosciences data processing. PB reads in SAM/BAM format are aligned
to a reference genome with the special-purpose aligner [pbmm2](https://github.com/PacificBiosciences/pbmm2>),
a modified version of [minimap2](https://lh3.github.io/minimap2/).
Methylation calls are then piled up from the aligned reads with [pb-CpG-tools](https://github.com/PacificBiosciences/pb-CpG-tools).

2. Oxford nanopore basecalling. ONT reads are optionally converted from FAST5
to [POD5](https://github.com/nanoporetech/pod5-file-format) format, then
basecalled and aligned to a reference with [dorado](https://github.com/nanoporetech/dorado>)
(dorado alignment also uses minimap2 under the hood), and finally piled up with
[modkit](https://github.com/nanoporetech/modkit).

3. Postprocessing and QC of methylation calls. Several functions are available
to generate diagnostic statistics and plots.

See also the [full documentation](https://salk-tm.gitlab.io/loreme/index.html).

Other tools of interest: [methylartist](https://github.com/adamewing/methylartist) and [modbamtools](https://github.com/rrazaghi/modbamtools)  ([modbamtools docs](https://rrazaghi.github.io/modbamtools/)), [methplotlib](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7214038/)

## Installation

### In a Conda environment

The recommended way to install `loreme` is with a dedicated `conda` environment:

First create an environment including all dependencies:
```sh
conda create -n loreme -c conda-forge -c bioconda samtools pbmm2 \
  urllib3 pybedtools gff2bed seaborn pyfaidx psutil gputil tabulate \
  cython h5py iso8601 more-itertools tqdm
conda activate loreme
```

Then install with `pip`:
```sh
pip install loreme
```

You may also wish to install `nvtop` to monitor GPU usage:
```sh
conda install -c conda-forge nvtop
```

### With pip

```sh
pip install loreme
```


### Check installation

Check that the correct version was installed with `loreme --version`

### Uninstall

To uninstall loreme:

```sh
loreme clean
pip uninstall loreme
```

## Oxford Nanopore reads

### Download dorado

Calling methylation from ONT long reads requires the basecaller [dorado](https://github.com/nanoporetech/dorado) . Download it by running

```
loreme download-dorado <platform>
```

This will download dorado and several basecalling models. The platform should be one of: `linux-x64`, `linux-arm64`, `osx-arm64`, `win64`, whichever matches your system. Running `loreme download-dorado --help` will show a hint as to the correct choice.

> #### Note
> For members of [Michael Lab](https://michael.salk.edu/) at Salk running on seabiscuit, use `loreme download-dorado linux-x64`.

### Modified basecalling

You can carry out modified basecalling (i.e. DNA methylation) with default parameters by running:

```
loreme dorado-basecall <pod5s/> <output.sam>
```

The input argument `pod5s/` should be a directory containing one or more POD5 files. For other parameter options, see `loreme dorado-basecall --help`

> #### Note
> Basecalling ONT data is disk-read intensive, so for best performance the input POD5 data should be on a fast SSD (For example, `/scratch/<username>` for members of [Michael Lab](https://michael.salk.edu/) at Salk).

To run dorado with only regular basecalling, use the `--no-mod` option:

```
loreme dorado-basecall --no-mod <pod5s/> <output.sam>
```

If you wish to convert the SAM file to a FASTQ file, use:
```
samtools view -bo output.bam output.sam
samtools fastq -T '*' output.bam > output.fq
```

### Alignment
The SAM file produced by dorado can be aligned to a reference index (FASTA or MMI file) with `loreme dorado-align`:

```
loreme dorado-align <index> <reads> <output.bam>
```

### Download modkit

Piling up methylation calls from BAM data requires [modkit](https://github.com/nanoporetech/modkit) . Download it by running:

```
loreme download-modkit
```

### Pileup

The pileup step generates a bedMethyl file from an aligned BAM file.

```
loreme modkit-pileup <reference.fasta> <input.bam> <output.bed>
```
> #### Note
> See `loreme modkit-pileup --help` for additional options. On a HPC system you may want to use additional threads with the `-t` flag.

### Postprocessing

See the [Pacific Biosciences reads](https://salk-tm.gitlab.io/loreme/pb_reads.html) section for examples of postprocessing analysis that can be applied to bedMethyl files.

