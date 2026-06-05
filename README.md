# Jobscript Generator

Command-line tool to generate Slurm jobscripts for scientific HPC workflows.
Uses Jinja2 templates with sensible defaults per software.

## Supported software

| Software | Default CPUs | Default Memory | Default Walltime |
|----------|-------------|----------------|-----------------|
| nwchem | 8 | 32G | 24h |
| gaussian | 16 | 64G | 48h |
| python_ml | 4 | 16G | 12h |

## Usage

    python3 jobgen.py --soft nwchem --input water.nw
    python3 jobgen.py --soft gaussian --input molecule.gjf --mem 64G --time 48h
    python3 jobgen.py --soft python_ml --input train.py --cpus 8 --mem 32G

## All options

    --soft        Software name (nwchem, gaussian, python_ml)
    --input       Input file
    --output      Output file (default: input.log)
    --mem         Memory (e.g. 32G)
    --time        Walltime (e.g. 24h or 24:00:00)
    --cpus        CPUs per task
    --partition   Slurm partition
    --version     Software version
    --out         Output jobscript filename

## Design

- Jinja2 templates in templates/ - one per software
- Sensible defaults per software based on real HPC usage
- Time format accepts both 24h and 24:00:00
- Scratch directory management for Gaussian
- OMP_NUM_THREADS set from SLURM_CPUS_PER_TASK

## Add a new software

1. Create templates/mysoftware.sh.j2
2. Add defaults in DEFAULTS dict in jobgen.py
3. Add to --soft choices
