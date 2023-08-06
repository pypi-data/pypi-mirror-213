import pysam
from itertools import islice

def check_tags(bam, n_reads: int = 1000):
    samfile = pysam.AlignmentFile(bam, 'r', check_sq=False)
    has_tags = any(((read.has_tag('MM') or read.has_tag('Mm'))
                    and (read.has_tag('ML') or read.has_tag('Ml'))
                    for read in islice(samfile.fetch(until_eof=True), n_reads)))
    samfile.close()
    return has_tags
