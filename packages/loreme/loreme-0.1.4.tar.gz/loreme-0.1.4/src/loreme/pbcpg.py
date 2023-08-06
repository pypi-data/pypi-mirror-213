import os
import subprocess
import pysam
from loreme.env import PBCPG_PATH, PBCPG_MODEL

def pbcpg_align_bam(ref: str, in_bam: str, out_bam: str, threads: int = 1,
              memory_mb: int = 768):
    """Run pbmm2 to align a BAM file to a FASTA reference

    Parameters
    ----------
    ref : str
        path to reference FASTA
    in_bam : str
        path to input BAM
    out_bam : str
        path to output BAM
    threads : int
        number of threads to use
    memory_mb : int
        megabytes of memory to use
    """
    subprocess.run(('pbmm2', 'align', '--preset', 'HIFI', '--sort',
                    '-j', f'{threads}', '--sort-memory', f'{memory_mb}M',
                    ref, in_bam, out_bam))


def pbcpg_align_bams(ref: str, in_bams, out_bam: str, threads: int = 1,
              memory_mb: int = 768):
    """Run pbmm2 to align a BAM file to a FASTA reference

    Parameters
    ----------
    ref : str
        path to reference FASTA
    in_bams : str
        paths to input BAMs
    out_bam : str
        path to output BAM
    threads : int
        number of threads to use
    memory_mb : int
        megabytes of memory to use
    """
    
    if len(in_bams) == 1:
        pbcpg_align_bam(ref, in_bams[0], out_bam, threads=threads,
                  memory_mb=memory_mb)
    else:
        for n, in_bam in enumerate(in_bams):
            pbcpg_align_bam(ref, in_bam, f'{out_bam[:-4]}_{n}.bam', threads=threads,
                    memory_mb=memory_mb)
        pysam.merge('-o', out_bam,
                    *(f'{out_bam[:-4]}_{n}.bam' for n in range(len(in_bams))))
        pysam.index(out_bam)
        for n in range(len(in_bams)):
            os.remove(f'{out_bam[:-4]}_{n}.bam')
            os.remove(f'{out_bam[:-4]}_{n}.bam.bai')

def pbcpg_pileup(bam, output_prefix, hap_tag: str = 'HP',
                  min_coverage: int = 4, min_mapq: int = 1,
                  model: str = PBCPG_MODEL, threads: int = 1):
    subprocess.run((PBCPG_PATH, '--bam', bam,
        '--output-prefix', output_prefix,
        '--hap-tag', hap_tag,
        '--min-coverage', str(min_coverage),
        '--min-mapq', str(min_mapq),
        '--model', model,
        '--threads', str(threads)))
