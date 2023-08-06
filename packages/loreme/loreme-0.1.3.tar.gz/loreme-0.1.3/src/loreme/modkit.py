import subprocess
from loreme.env import MODKIT_PATH

def modkit_pileup(fasta: str, input_bam: str, output_bed: str, log=None,
                  threads: int = 1):
    subprocess.run((MODKIT_PATH, 'pileup', input_bam, output_bed, '--ref', fasta,
                    '--threads', str(threads), '--preset', 'traditional')
                   + bool(log)*('--log-filepath', log))
