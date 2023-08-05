# zgtf
gtf conversion utlity

# Installation

```bash
# clone the repo
git clone https://github.com/zavolanlab/zgtf.git
# create a virtual environment
python3 -m venv venv
# activate the virtual environment
source venv/bin/activate
# install zgtf scripts
pip install .
```

# Run

Convert gtf file to bed12
```bash
gtf2bed12 --gtf <INPUT.gtf> --bed12 <OUTPUT.bed> --verbose
```

```
arguments:
  -h, --help            show this help message and exit
  --gtf FILE            Annotation file (gtf format)
  --bed12 FILE          Output file (bed12 format)
  --transcript_type TRANSCRIPT_TYPE
                        Transcript type [Default: protein_coding]
  -v, --verbose         Verbose
  ```

# Docker 

Pull image
```bash
docker pull zavolab/zgtf
```

Run
```bash
docker run -it zavolab/zgtf gtf2bed12 --help
```

# Singularity

Pull image
```bash
singularity pull docker://zavolab/zgtf
```

Run
```bash
singularity exec zgtf_latest.sif gtf2bed12 --help
```