import itertools
import os
import os.path
import subprocess
import pysam
import multiprocessing
from loreme.env import DORADO_PATH, DORADO_PATH_024, DORADO_MODEL_DIR, DORADO_PLATFORM

CPU_COUNT = multiprocessing.cpu_count()

def fast5_to_pod5(*input_fast5, output_pod5: str, threads: int = 1):
    """Convert FAST5 files to POD5 files

    Parameters
    ----------
    *input_fast5
        fast5 files or directories containing fast5s
    output_pod5 : str
        output POD5 file
    """

    parsed_fast5 = itertools.chain.from_iterable(
        ([os.path.join(f, f5) for f5 in os.listdir(f) if f5.endswith('.fast5')]
         if os.path.isdir(f) else [f]) for f in input_fast5)
    subprocess.run(('pod5', 'convert', 'fast5', *parsed_fast5,
                    '--output', output_pod5, '--threads', str(threads)))


def dorado_basecall(input_dir, output, speed: int = 400, accuracy: str ='fast',
           frequency: str = '4kHz', modified_bases: str = '5mCG_5hmCG',
           no_mod: bool = False, reference=None):
    """Run dorado basecaller

    Parameters
    ----------
    input_dir : str
        directory containing POD5 or Fast5 files
    output : str
        path to output BAM file
    speed : int
        pore speed, either 260 or 400 (default: 400)
    accuracy : str
        model accuracy, one of fast, hac, or sup (default: fast)
    frequency : str
        either 4kHz or 5kHz (default: 4kHz)
    modified_bases : str
        modified base model to use, one of 5mCG_5hmCG, 5mC, 6mA
        (default: 5mCG_5hmCG)
    reference : str
        path to reference index for alignment
    """

    if speed not in {260, 400}:
        raise RuntimeError('Invalid speed choice. Choose 400 or 260.')
    if accuracy not in {'fast', 'hac', 'sup'}:
        raise RuntimeError('Invalid accuracy choice. Choose fast, hac, or sup.')
    if frequency not in {'4kHz', '5kHz'}:
        raise RuntimeError('Invalid frequency choice. Choose 4kHz or 5kHz.')
    if modified_bases not in {'5mCG_5hmCG', '5mC', '6mA'}:
        raise RuntimeError('Invalid modified bases choice. Choose 5mCG_5hmCG, 5mC, 6mA.')
    if speed == 260 and frequency != '4kHz':
        raise RuntimeError('260bps speed only available at 4kHz frequency')
    if frequency == '4kHz' and modified_bases != '5mCG_5hmCG':
        raise RuntimeError('the only modified base model at 4kHz frequency is 5mCG_5hmCG')
    model = f"dna_r10.4.1_e8.2_{speed}bps_{accuracy}@v4.{1+(frequency=='5kHz')}.0"
    with open(output, 'wb') as f:
        subprocess.run((DORADO_PATH_024[DORADO_PLATFORM], 'basecaller',
                        os.path.join(DORADO_MODEL_DIR, model), input_dir)
                        + (not no_mod) * ('--modified-bases', modified_bases)
                        + bool(reference) * ('--reference', reference),
                       stdout=f)


def dorado_align(reference_index: str, input_reads: str, output_bam: str,
                 threads: int = CPU_COUNT, mem_per_thread_mb: int = 768):
    """Run dorado aligner, sorting and indexing the output

    Parameters
    ----------
    reference_index : str
        path to reference index
    input_reads : str
        path to input reads
    output_bam : str
        path to output BAM file
    """

    with open(output_bam, 'wb') as f, \
        subprocess.Popen((DORADO_PATH[DORADO_PLATFORM], 'aligner',
            reference_index, input_reads), stdout=subprocess.PIPE) as aligner:
        subprocess.run(('samtools', 'sort', '-@', str(threads),
                        '-m', f'{mem_per_thread_mb}M'),
                       stdin=aligner.stdout, stdout=f)
    pysam.index(output_bam)
