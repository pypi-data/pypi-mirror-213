import os
import os.path

PBCPG_DIR = os.environ.get('LOREME_PBCPG_DIR',
    os.path.join(os.path.dirname(__file__)))
PBCPG_PATH = os.path.join(PBCPG_DIR, 'pb-CpG-tools-v2.3.1-x86_64-unknown-linux-gnu',
                         'bin', 'aligned_bam_to_cpg_scores')
PBCPG_MODEL = os.path.join(PBCPG_DIR, 'pb-CpG-tools-v2.3.1-x86_64-unknown-linux-gnu',
                               'models', 'pileup_calling_model.v1.tflite')
PBCPG_URL = 'https://github.com/PacificBiosciences/pb-CpG-tools/releases/download/v2.3.1/pb-CpG-tools-v2.3.1-x86_64-unknown-linux-gnu.tar.gz'
EXAMPLE_DATA_URLS = (
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64011_190830_220126.hifi_reads.bam',
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64011_190901_095311.hifi_reads.bam',
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64012_190920_173625.hifi_reads.bam',
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64012_190921_234837.hifi_reads.bam',
)
HG38_FTP = 'ftp.ncbi.nlm.nih.gov'
HG38_GENOME_PATH = 'genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz'
HG38_ANNOT_PATH = 'genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.gff.gz'
EXAMPLE_DATA_DIR = os.environ.get('LOREME_EXAMPLE_DATA_DIR', os.path.dirname(__file__))

DORADO_DIR = os.environ.get('LOREME_DORADO_DIR',
    os.path.join(os.path.dirname(__file__)))
DORADO_PLATFORM = os.environ.get('LOREME_DORADO_PLATFORM')
DORADO_PATH = {
    'linux-x64': os.path.join(DORADO_DIR, 'dorado-0.3.0-linux-x64', 'bin', 'dorado'),
    'linux-arm64': os.path.join(DORADO_DIR, 'dorado-0.3.0-linux-arm64', 'bin', 'dorado'),
    'osx-arm64': os.path.join(DORADO_DIR, 'dorado-0.3.0-osx-arm64', 'bin', 'dorado'),
    'win64': os.path.join(DORADO_DIR, 'dorado-0.3.0-win64', 'bin', 'dorado')
}
DORADO_PATH_024 = {
    'linux-x64': os.path.join(DORADO_DIR, 'dorado-0.2.4-linux-x64', 'bin', 'dorado'),
    'linux-arm64': os.path.join(DORADO_DIR, 'dorado-0.2.4-linux-arm64', 'bin', 'dorado'),
    'osx-arm64': os.path.join(DORADO_DIR, 'dorado-0.2.4-osx-arm64', 'bin', 'dorado'),
    'win64': os.path.join(DORADO_DIR, 'dorado-0.2.4-win64', 'bin', 'dorado')
}
DORADO_URL = {
    'linux-x64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.3.0-linux-x64.tar.gz',
    'linux-arm64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.3.0-linux-arm64.tar.gz',
    'osx-arm64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.3.0-osx-arm64.tar.gz',
    'win64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.3.0-win64.zip'
}
DORADO_URL_024 = {
    'linux-x64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.2.4-linux-x64.tar.gz',
    'linux-arm64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.2.4-linux-arm64.tar.gz',
    'osx-arm64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.2.4-osx-arm64.tar.gz',
    'win64': 'https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.2.4-win64.zip'
}
DORADO_MODEL_DIR = os.environ.get('LOREME_DORADO_MODEL_DIR',
    os.path.join(os.path.dirname(__file__)))
